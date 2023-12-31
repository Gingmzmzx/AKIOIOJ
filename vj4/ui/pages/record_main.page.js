import { NamedPage } from 'vj/misc/PageLoader';
import UserSelectAutoComplete from 'vj/components/autocomplete/UserSelectAutoComplete';

const page = new NamedPage('record_main', async () => {
  const { default: SockJs } = await import('sockjs-client');
  const { DiffDOM } = await import('diff-dom');

  const sock = new SockJs(Context.socketUrl);
  const dd = new DiffDOM();

  let heartbeatClock;
  sock.onopen = () => {
    heartbeatClock = setInterval(() => {
      sock.send(JSON.stringify({}));  // heartbeat
    }, 25000);
  };
  sock.onclose = () => clearInterval(heartbeatClock);

  sock.onmessage = message => {
    const msg = JSON.parse(message.data);
    const $newTr = $(msg.html);
    const $oldTr = $(`.record_main__table tr[data-rid="${$newTr.attr('data-rid')}"]`);
    if ($oldTr.length) {
      $oldTr.trigger('vjContentRemove');
      dd.apply($oldTr[0], dd.diff($oldTr[0], $newTr[0]));
      $oldTr.trigger('vjContentNew');
    } else {
      $('.record_main__table tbody').prepend($newTr);
      $newTr.trigger('vjContentNew');
    }
  };

  UserSelectAutoComplete.getOrConstruct($('.filter-user [name="uid_or_name"]'), {
    clearDefaultValue: false,
  });
});

export default page;
