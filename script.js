function showPage(pageId) {
    // 隐藏所有页面
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.style.display = 'none'; // 隐藏每个页面
    });

    // 显示指定页面
    const activePage = document.getElementById(pageId);
    if (activePage) {
        activePage.style.display = 'block'; // 显示所选页面
    }
}

// 默认显示首页
document.addEventListener("DOMContentLoaded", function() {
    showPage('home');
});

function toggleVersions(projectNameElement) {
    // 找到当前项目下的版本列表
    const versions = projectNameElement.nextElementSibling;

    // 切换显示状态
    if (versions.style.display === 'none') {
        versions.style.display = 'block'; // 显示版本
    } else {
        versions.style.display = 'none'; // 隐藏版本
    }
}
