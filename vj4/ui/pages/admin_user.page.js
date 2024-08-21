import _ from 'lodash';

import { NamedPage } from 'vj/misc/PageLoader';
import Notification from 'vj/components/notification';
import { ConfirmDialog, ActionDialog } from 'vj/components/dialog';
import UserSelectAutoComplete from 'vj/components/autocomplete/UserSelectAutoComplete';

import request from 'vj/utils/request';

const page = new NamedPage('admin_user', () => {
  const setBadgeSelector = UserSelectAutoComplete.getOrConstruct($('.dialog__body--set-badge [name="user"]'));
  const setBadgeDialog = new ActionDialog({
    $body: $('.dialog__body--set-badge > div'),
    onDispatch(action) {
      const $badge = setBadgeDialog.$dom.find('[name="badge"]');
      if (action === 'ok') {
        if (setBadgeSelector.value() === null) {
          setBadgeSelector.focus();
          return false;
        }
      }
      return true;
    },
  });
  setBadgeDialog.clear = function () {
    setBadgeSelector.clear();
    this.$dom.find('[name="badge"]').val('');
    return this;
  };

  async function handleClickSetBadge(ev) {
    const row = $(ev.currentTarget).closest('tr');
    const uid = row.attr('data-uid');
    const badge = row.attr('data-badge');
    setBadgeDialog.$dom.find('[name="badge"]').val(badge);
    setBadgeSelector.$dom.val(uid);
    setBadgeSelector._value = {"_id":uid};
    const action = await setBadgeDialog.open();
    if (action !== 'ok') {
      return;
    }
    const nuid = setBadgeSelector.value()['_id'];
    console.log(nuid);
    const nbadge = setBadgeDialog.$dom.find('[name="badge"]').val();
    try {
      await request.post('', {
        operation: 'set_badge',
        uid: nuid,
        badge: nbadge,
      });
      window.location.reload();
    } catch (error) {
      Notification.error(error.message);
    }
  }

  $('[name="set_badge"]').click(ev => handleClickSetBadge(ev));
});

export default page;
