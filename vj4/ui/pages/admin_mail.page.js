import _ from 'lodash';

import { NamedPage } from 'vj/misc/PageLoader';
import Notification from 'vj/components/notification';
import { ConfirmDialog } from 'vj/components/dialog';

import request from 'vj/utils/request';
import tpl from 'vj/utils/tpl';
import delay from 'vj/utils/delay';
import i18n from 'vj/utils/i18n';

const page = new NamedPage('admin_mail', () => {
  function ensureAndGetSelectedUsers() {
    const users = _.map(
      $('.admin_user_list tbody [type="checkbox"]:checked'),
      ch => $(ch).closest('tr').attr('data-uid'),
    );
    if (users.length === 0) {
      Notification.error(i18n('Please select at least one user to perform this operation.'));
      return null;
    }
    return users;
  }

  async function sendMail(uid, title, content){
    try {
      await request.post('', {
        operation: 'send_mail',
        uid: uid,
        title: title,
        content: content
      });
      Notification.success(i18n('Mail successfully sent to uid:{0}.', uid));
    } catch (error) {
      Notification.error(`Error uid:${uid} ${error.message}`);
    }
  }

  async function handleClickSend() {
    const selectedUsers = ensureAndGetSelectedUsers();
    if (selectedUsers === null) {
      return;
    }
    const action = await new ConfirmDialog({
      $body: tpl`
        <div class="typo">
          <p>${i18n('Confirm sending Email to selected users?')}</p>
        </div>`,
    }).open();
    if (action !== 'yes') {
      return;
    }
    const mail_content_container = $("#mail_content_container");
    const mail_title = mail_content_container.find('[name="title"]').val();
    const mail_content = mail_content_container.find('[name="content"]').val();
    _.map(selectedUsers, async ch => { await sendMail(ch, mail_title, mail_content)});
  }


  $('[name="btn_send_mail"]').click(() => handleClickSend());
});

export default page;
