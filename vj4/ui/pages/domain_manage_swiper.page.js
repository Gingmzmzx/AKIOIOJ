import _ from 'lodash';

import { NamedPage } from 'vj/misc/PageLoader';
import Notification from 'vj/components/notification';
import { ConfirmDialog, ActionDialog } from 'vj/components/dialog';

import request from 'vj/utils/request';

const page = new NamedPage('domain_manage_swiper', () => {
  const AddSwiperImageDialog = new ActionDialog({
    $body: $('.dialog__body--addSwiperImage > div'),
    onDispatch(action) {
      const $src = AddSwiperImageDialog.$dom.find('[name="src"]');
      const $href = AddSwiperImageDialog.$dom.find('[name="href"]');
      if (action === 'ok') {
        if ($src.val() === null) {
          $src.focus();
          return false;
        }
        if ($href.val() === null) {
            $href.focus();
            return false;
          }
      }
      return true;
    },
  });
  AddSwiperImageDialog.clear = function () {
    this.$dom.find('[name="src"]').val('');
    this.$dom.find('[name="href"]').val('');
    return this;
  };

  async function handleClickAddSwiperImageDialog() {
    const action = await AddSwiperImageDialog.clear().open();
    if (action !== 'ok') {
      return;
    }
    const src = AddSwiperImageDialog.$dom.find('[name="src"]').val();
    const href = AddSwiperImageDialog.$dom.find('[name="href"]').val();
    try {
      await request.post('', {
        operation: 'add_image',
        src: src,
        href,
      });
      window.location.reload();
    } catch (error) {
      Notification.error(error.message);
    }
  }

  async function handleClickDeleteImage(ev){
    const row = $(ev.currentTarget).closest('tr');
    const src = row.attr('data-src');

    try {
        await request.post('', {
          operation: 'del_image',
          src: src,
        });
        window.location.reload();
      } catch (error) {
        Notification.error(error.message);
      }
  }

  $('[name="add_image"]').click(() => handleClickAddSwiperImageDialog());
  $('[name="delete"]').click((ev) => handleClickDeleteImage(ev));
});

export default page;
