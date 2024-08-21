from vj4 import app
from vj4 import error
from vj4.model import builtin
from vj4.model import user
from vj4.handler import base


@app.route('/admin', 'admin')
class AdminManageHandler(base.Handler):
  async def get(self):
    self.redirect(self.reverse_url('admin_dashboard'))


@app.route('/admin/dashboard', 'admin_dashboard')
class AdminDashboardHandler(base.Handler):
  async def get(self):
    if not self.has_priv(builtin.PRIV_ADMIN):
      self.check_priv(builtin.PRIV_ADMIN)
    self.render('admin_dashboard.html')


@app.route('/admin/user', 'admin_user')
class AdminUserHandler(base.OperationHandler):
  @base.require_priv(builtin.PRIV_ADMIN)
  async def get(self):
    udocs = []
    async for udoc in user.get_multi():
      udocs.append(udoc)

    self.render('admin_user.html', udocs=udocs)

  @base.require_priv(builtin.PRIV_ADMIN)
  @base.require_csrf_token
  @base.sanitize
  async def post_set_badge(self, *, uid: int, badge: str):
    await user.set_tags(uid, badge.split())
    self.json_or_redirect(self.url)


@app.route('/admin/privilege/{uid:-?\d+}', 'admin_privilege')
class AdminPrivilegeHandler(base.Handler):
  @base.require_priv(builtin.PRIV_ADMIN)
  @base.route_argument
  @base.sanitize
  async def get(self, *, uid: int):
    def bitand(a, b):
      return a & b
    # unmodifiable roles are not visible in UI so that we are not using get_all_roles() here
    udoc = await user.get_by_uid(uid)
    self.render('admin_privilege.html', bitand=bitand, udoc=udoc)

  @base.require_priv(builtin.PRIV_ADMIN)
  @base.route_argument
  async def post(self, *, uid: int):
    args = await self.request.post()
    if self.csrf_token and self.csrf_token != args.get('csrf_token', ''):
      raise error.CsrfTokenError()
    privs = 0
    for priv in args.getall("priv", []):
      priv = int(priv)
      if priv in builtin.PRIVS_BY_KEY:
        privs |= priv
    await user.set_priv(int(uid), privs)
    self.json_or_redirect(self.reverse_url("admin_user"))

