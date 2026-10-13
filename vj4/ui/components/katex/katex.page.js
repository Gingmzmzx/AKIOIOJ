import { AutoloadPage } from 'vj/misc/PageLoader';

import 'katex/dist/katex.min.css';
import './katex.styl';

const katexPage = new AutoloadPage('katexPage', () => {
  import('katex/dist/contrib/auto-render.min.js').then(renderKatex => {
    // auto-render picks the first delimiter that matches, so `$$` has to come
    // before `$`. The single dollar form is not a default, since it collides
    // with literal dollar signs in prose.
    const options = {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
        { left: '$', right: '$', display: false },
      ],
    };
    function runKatex($containers) {
      $containers.get().forEach(container => renderKatex.default(container, options));
    }
    runKatex($('.typo'));
    $(document).on('vjContentNew', e => runKatex($(e.target).find('.typo')));
  });
});

export default katexPage;
