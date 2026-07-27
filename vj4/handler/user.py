import asyncio
import datetime
import secrets
import logging
from urllib import parse

import aiohttp
from bson import objectid

from vj4 import app
from vj4 import constant
from vj4 import error
from vj4.model import builtin
from vj4.model import domain
from vj4.model import record
from vj4.model import system
from vj4.model import token
from vj4.model import user
from vj4.model.adaptor import discussion
from vj4.model.adaptor import problem
from vj4.model.adaptor import setting
from vj4.util import misc
from vj4.util import options
from vj4.handler import base

_logger = logging.getLogger(__name__)


class UserSettingsMixin(object):
  def can_view(self, udoc, key):
    privacy = udoc.get('show_' + key, next(iter(setting.SETTINGS_BY_KEY['show_' + key].range)))
    return udoc['_id'] == self.user['_id'] \
           or (privacy == constant.setting.PRIVACY_PUBLIC and True) \
           or (privacy == constant.setting.PRIVACY_REGISTERED_ONLY
               and self.has_priv(builtin.PRIV_USER_PROFILE)) \
           or (privacy == constant.setting.PRIVACY_SECRET
               and self.has_priv(builtin.PRIV_VIEW_USER_SECRET))

  def get_udoc_setting(self, udoc, key):
    if self.can_view(udoc, key):
      return udoc.get(key, None)
    else:
      return None


@app.route('/login', 'user_login', global_route=True)
class UserLoginHandler(base.Handler):
  """Redirect user to NetEssX OAuth authorization endpoint."""

  SCOPE = 'user:profile user:email'

  async def get(self):
    if self.has_priv(builtin.PRIV_USER_PROFILE):
      self.redirect(self.reverse_url('domain_main'))
      return
    if not options.oauth_client_id or not options.oauth_client_secret:
      raise error.UserFacingError('OAuth is not configured.')
    state = secrets.token_urlsafe(32)
    self.session['oauth_state'] = state
    params = {
      'client_id': options.oauth_client_id,
      # 'redirect_uri': options.url_prefix.rstrip('/') + '/oauth/callback',
      'redirect_uri': 'http://127.0.0.1:8888/oauth/callback',
      'response_type': 'code',
      'scope': self.SCOPE,
      'state': state,
    }
    auth_url = options.oauth_auth_base.rstrip('/') + '/oauth/authorize?' + parse.urlencode(params)
    self.redirect(auth_url)


@app.route('/oauth/callback', 'oauth_callback', global_route=True)
class OAuthCallbackHandler(base.Handler):
  """Handle OAuth callback from NetEssX, exchange code for token, and create/login user."""

  async def get(self):
    code = self.request.query.get('code')
    state = self.request.query.get('state')
    error_param = self.request.query.get('error')

    # Handle denied authorization
    if error_param:
      _logger.warning('OAuth authorization denied: %s', error_param)
      self.render('user_login.html', oauth_error=error_param)
      return

    if not code:
      raise error.ValidationError('code')

    # Verify state for CSRF protection
    saved_state = self.session.get('oauth_state')
    if saved_state and state != saved_state:
      _logger.warning('OAuth state mismatch: expected %s, got %s', saved_state, state)
      raise error.ValidationError('state')

    # Exchange code for access token
    token_data = await self._exchange_code(code)
    access_token = token_data.get('access_token')
    if not access_token:
      _logger.error('OAuth token exchange failed: %s', token_data)
      raise error.UserFacingError('Failed to obtain access token.')

    # Fetch user info from NetEssX API
    user_data = await self._fetch_user_info(access_token)
    if not user_data:
      raise error.UserFacingError('Failed to fetch user info.')

    _logger.debug('User info: %s', user_data)

    oauth_uid = str(user_data.get('uid'))
    uname = user_data.get('uname', '')
    gravatar = user_data.get('gravatar', '')
    mail = user_data.get('mail', '')

    # Find or create local user
    udoc = await user.get_by_oauth_uid(oauth_uid)
    if not udoc:
      # Create a new user from OAuth data
      try:
        uid = await user.add_by_oauth(
          oauth_uid=oauth_uid,
          uname=uname,
          mail=mail,
          gravatar=gravatar or options.default_avatar,
          regip=self.remote_ip,
        )
      except error.UserAlreadyExistError:
        # Fallback: try to find by uname
        udoc = await user.get_by_uname(uname)
        if not udoc:
          raise
        uid = udoc['_id']
    else:
      uid = udoc['_id']
      # Update gravatar on re-login
      if gravatar:
        await user.set_by_uid(uid, gravatar=gravatar)

    # Update login info and create session
    await asyncio.gather(
      user.set_by_uid(uid, loginat=datetime.datetime.utcnow(), loginip=self.remote_ip),
      self.update_session(new_saved=True, uid=uid),
    )

    # Clear OAuth state
    self.session.pop('oauth_state', None)

    self.redirect(self.reverse_url('domain_main'))

  async def _exchange_code(self, code: str) -> dict:
    """Exchange authorization code for access token."""
    auth_base = options.oauth_auth_base.rstrip('/')
    url = auth_base + '/oauth/token'
    data = {
      'grant_type': 'authorization_code',
      'code': code,
      # 'redirect_uri': options.url_prefix.rstrip('/') + '/oauth/callback',
      'redirect_uri': 'http://127.0.0.1:8888/oauth/callback',
      'client_id': options.oauth_client_id,
      'client_secret': options.oauth_client_secret,
    }
    _logger.debug('Sending authorization request: %s', data)
    async with aiohttp.ClientSession() as session:
      async with session.post(url, data=data) as resp:
        return await resp.json()

  async def _fetch_user_info(self, access_token: str) -> dict:
    """Fetch user info from NetEssX API using access token."""
    auth_base = options.oauth_auth_base.rstrip('/')
    url = auth_base + '/api/user/me'
    headers = {'Authorization': 'Bearer ' + access_token}
    async with aiohttp.ClientSession() as session:
      async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
          _logger.error('Failed to fetch user info: %s', await resp.text())
          return {}
        return await resp.json()


@app.route('/logout', 'user_logout', global_route=True)
class UserLogoutHandler(base.Handler):
  @base.require_priv(builtin.PRIV_USER_PROFILE)
  async def get(self):
    self.render('user_logout.html')

  @base.require_priv(builtin.PRIV_USER_PROFILE)
  async def post(self):
    await self.delete_session()
    self.json_or_redirect(self.referer_or_main)


@app.route('/user/{uid:-?\d+}', 'user_detail')
class UserDetailHandler(base.Handler, UserSettingsMixin):
  @base.route_argument
  @base.sanitize
  async def get(self, *, uid: int):
    is_self_profile = self.has_priv(builtin.PRIV_USER_PROFILE) and self.user['_id'] == uid
    udoc = await user.get_by_uid(uid)
    if not udoc:
      raise error.UserNotFoundError(uid)
    dudoc, sdoc = await asyncio.gather(domain.get_user(self.domain_id, udoc['_id']),
                                       token.get_most_recent_session_by_uid(udoc['_id']))

    rdocs = record.get_multi(get_hidden=self.has_priv(builtin.PRIV_VIEW_HIDDEN_RECORD),
                             uid=uid).sort([('_id', -1)])
    rdocs = await rdocs.limit(10).to_list()
    pdict = await problem.get_dict_multi_domain((rdoc['domain_id'], rdoc['pid']) for rdoc in rdocs)

    # check hidden problem
    if not self.has_perm(builtin.PERM_VIEW_PROBLEM_HIDDEN):
      f = {'hidden': False}
    else:
      f = {}
    pdocs = problem.get_multi(domain_id=self.domain_id, owner_uid=uid, **f).sort([('_id', -1)])
    pcount = await pdocs.count()
    pdocs = await pdocs.limit(10).to_list()

    psdocs = problem.get_multi_solution_by_uid(self.domain_id, uid)
    psdocs_hot = problem.get_multi_solution_by_uid(self.domain_id, uid)
    pscount = await psdocs.count()
    psdocs = await psdocs.limit(10).to_list()
    psdocs_hot = await psdocs_hot.sort([('vote', -1), ('doc_id', -1)]).limit(10).to_list()

    if self.has_perm(builtin.PERM_VIEW_DISCUSSION):
      benbenid = None
      ddocs = None
      for dom in builtin.DOMAINS:
        if dom['_id'] == self.domain_id:
          benbenid = await system.get_benbenid()
          ddocs = discussion.get_multi(self.domain_id, owner_uid=uid, doc_id={"$ne":objectid.ObjectId(benbenid)})
          break
      else:
        ddocs = discussion.get_multi(self.domain_id, owner_uid=uid)
      dcount = await ddocs.count()
      ddocs = await ddocs.limit(10).to_list()
      vndict = await discussion.get_dict_vnodes(self.domain_id, map(discussion.node_id, ddocs))
    else:
      ddocs = []
      vndict = {}
      dcount = 0
    
    self.render('user_detail.html', is_self_profile=is_self_profile,
                udoc=udoc, dudoc=dudoc, sdoc=sdoc,
                rdocs=rdocs, pdict=pdict, pdocs=pdocs, pcount=pcount,
                psdocs=psdocs, pscount=pscount, psdocs_hot=psdocs_hot,
                ddocs=ddocs, dcount=dcount, vndict=vndict)


@app.route('/user/{uid:-?\d+}/set_cheat', 'user_set_cheat')
class UserCheatHandler(base.Handler, UserSettingsMixin):
  @base.route_argument
  @base.sanitize
  @base.require_priv(builtin.PRIV_USER_SET_CHEAT)
  async def get(self, *, uid: int):
    udoc = await user.get_by_uid(uid)
    if not udoc:
      raise error.UserNotFoundError(uid)
    status = not udoc.get("cheater", False)
    await user.set_cheat(uid, status)

    self.json_or_redirect(self.reverse_url('user_detail', uid=uid))


@app.route('/user/{uid:-?\d+}/set_memorial_account', 'user_set_memorial_account')
class UserMemorialAccountHandler(base.Handler, UserSettingsMixin):
  @base.route_argument
  @base.sanitize
  @base.require_priv(builtin.PRIV_USER_SET_MEMORIAL_ACCOUNT)
  async def get(self, *, uid: int):
    udoc = await user.get_by_uid(uid)
    if not udoc:
      raise error.UserNotFoundError(uid)
    status = not udoc.get("commemorate", False)
    await user.set_commemorate(uid, status)

    self.json_or_redirect(self.reverse_url('user_detail', uid=uid))


@app.route('/user/search', 'user_search')
class UserSearchHandler(base.Handler):
  def modify_udoc(self, udict, key):
    udoc = udict[key]
    gravatar_url = misc.gravatar_url(udoc.get('gravatar'))
    if 'gravatar' in udoc and udoc['gravatar']:
      udict[key] = {**udoc,
                    'gravatar_url': gravatar_url,
                    'gravatar': ''}

  @base.require_priv(builtin.PRIV_USER_PROFILE)
  @base.get_argument
  @base.route_argument
  @base.sanitize
  async def get(self, *, q: str, exact_match: bool=False):
    if exact_match:
      udocs = []
    else:
      udocs = await user.get_prefix_list(q, user.PROJECTION_PUBLIC, 20)
    try:
      udoc = await user.get_by_uid(int(q), user.PROJECTION_PUBLIC)
      if udoc:
        udocs.insert(0, udoc)
    except ValueError as e:
      pass
    for i in range(len(udocs)):
      self.modify_udoc(udocs, i)
    self.json(udocs)
