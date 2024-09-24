/*
 * update tab front background color
 */
function update_current_tab_color(all_tabs, name)
{
    all_tabs.forEach(tab => {
        if (tab.innerText == "Site") {
            tab.classList.remove('active');
        } else if (tab.innerText.split(' ')[0] == name) {
            tab.classList.add('active');
        }
    });
}
