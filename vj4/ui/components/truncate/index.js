import i18n from 'vj/utils/i18n';

export default class Truncate {
  constructor(selector, maxHeightPercentage) {
    const containers = document.querySelectorAll(selector);

    containers.forEach(container => {
      const mask = document.createElement('div');
      mask.className = 'truncate-mask';
      container.appendChild(mask);

      const maxHeight = (maxHeightPercentage / 100) * window.innerHeight; // 根据百分比计算最大高度
      let isExpanded = false;

      this.checkHeight(container, mask, maxHeight);

      if (container.scrollHeight > maxHeight) {
        const button = document.createElement('button');
        button.className = 'truncate-toggle-button';
        button.innerHTML = `<span class="icon icon-expand_more"></span>${i18n("Expand")}`;
        container.appendChild(button);
        button.addEventListener('click', () => {
          isExpanded = this.toggleContent(container, mask, button, maxHeight, isExpanded);
        });
      }

      window.addEventListener('resize', () => this.checkHeight(container, mask, maxHeight));
    });
  }

  checkHeight(container, mask, maxHeight) {
    if (container.scrollHeight > maxHeight) {
      container.style.maxHeight = maxHeight + 'px';
      mask.classList.add('visible'); // 显示遮罩
    } else {
      container.style.maxHeight = 'none';
      mask.classList.remove('visible'); // 隐藏遮罩
    }
  }

  toggleContent(container, mask, button, maxHeight, isExpanded) {
    if (isExpanded) {
      container.style.maxHeight = maxHeight + 'px';
      mask.classList.add('visible'); // 显示遮罩
      button.innerHTML = `<span class="icon icon-expand_more"></span>${i18n("Expand")}`;
    } else {
      const fullHeight = container.scrollHeight + 'px'; // 动态获取完整高度
      container.style.maxHeight = fullHeight;
      mask.classList.remove('visible'); // 隐藏遮罩
      button.innerHTML = `<span class="icon icon-expand_less"></span>${i18n("Collapse")}`;
    }
    return !isExpanded; // 返回更新后的状态
  }
}
