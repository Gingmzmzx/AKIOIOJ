import _ from 'lodash';

import { NamedPage } from 'vj/misc/PageLoader';
import Notification from 'vj/components/notification';
import { ConfirmDialog, ActionDialog } from 'vj/components/dialog';

import request from 'vj/utils/request';

const page = new NamedPage('domain_manage_suggest_problem', () => {
  const AddSProblemDialog = new ActionDialog({
    $body: $('.dialog__body--add > div'),
    onDispatch(action) {
      const $pid = AddSProblemDialog.$dom.find('[name="pid"]');
      const $title = AddSProblemDialog.$dom.find('[name="title"]');
      if (action === 'ok') {
        if ($pid.val() === null) {
          $pid.focus();
          return false;
        }
        if ($title.val() === null) {
            $title.focus();
            return false;
          }
      }
      return true;
    },
  });
  AddSProblemDialog.clear = function () {
    this.$dom.find('[name="pid"]').val('');
    this.$dom.find('[name="title"]').val('');
    return this;
  };

  async function handleClickAddSProblemDialog() {
    const action = await AddSProblemDialog.clear().open();
    if (action !== 'ok') {
      return;
    }
    const pid = AddSProblemDialog.$dom.find('[name="pid"]').val();
    const title = AddSProblemDialog.$dom.find('[name="title"]').val();
    try {
      await request.post('', {
        operation: 'add_problem',
        pid: pid,
        title,
      });
      window.location.reload();
    } catch (error) {
      Notification.error(error.message);
    }
  }

  async function handleClickDelete(ev){
    const row = $(ev.currentTarget).closest('tr');
    const pid = row.attr('data-pid');

    try {
        await request.post('', {
          operation: 'del_problem',
          pid: pid,
        });
        window.location.reload();
      } catch (error) {
        Notification.error(error.message);
      }
  }

  $('[name="add_problem"]').click(() => handleClickAddSProblemDialog());
  $('[name="delete"]').click((ev) => handleClickDelete(ev));
});

export default page;
