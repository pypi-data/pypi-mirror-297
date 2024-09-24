/*
 * Quick search for the SDA List table in dcim/sites/ voice tab
 */
function init_voice_quick_search(quicksearch)
{
    const query = quicksearch.value;
    const columns = Array.from(document.querySelectorAll('#DIDs th'));
    const rows = Array.from(document.querySelectorAll('#DIDs tbody tr'));
    const headers = Array.from(document.querySelectorAll('#DIDs thead th'));

    let start = null;
    let end = null;
    let start_index = -1;
    let end_index = -1;

    /*
     * finds start and end columns
     */
    columns.forEach(th => {
        if (!start) {
            start = (lower_case(th.textContent.trim()) === "start number") ? th : null;
        }
        if (!end) {
            end = (lower_case(th.textContent.trim()) === "end number") ? th : null;
        }
    });

    /*
     * finds start and end index
     */
    headers.forEach((header, index) => {
        const tmp_txt = lower_case(header.innerText.trim());

        if (tmp_txt === lower_case(start.innerText.trim())) {
            start_index = index;
        }
        if (tmp_txt === lower_case(end.innerText.trim())) {
            end_index = index;
        }
    });

    /*
     * simple occurrence algorithm
     * to search for the query in the range between start and end
     */
    rows.forEach(row => {
        const cell = row.querySelectorAll('td');
        const r1 = cell[start_index].innerText;
        const r2 = cell[end_index].innerText;

        if (query === '') {
            row.style.display = '';
        } else if (format_data(r1, r2, query)) {
            row.style.display = '';
        } else if (strstr(r1, query) || strstr(r2, query)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
        
    function is_digit(c)
    {
        return c >= '0' && c <= '9';
    }    

    function extract_digits(str)
    {
        return str.split('').filter(is_digit).join('');
    }

    function has_digit(str)
    {
        return str.split('').some(is_digit);
    }

    /*
     * simply converts a string to an int
     * had to be done like this because of javascript
     */
    function str_to_int(str)
    {
        if (has_digit(str)) {
            return parseInt(extract_digits(str), 10);
        } else {
            return str;
        }
    }

     function compare_str(haystack, needle, i, l2)
    {
        let j = 0;
    
        for (; j < l2; j++) {
            if (haystack[i + j] !== needle[j]) {
                break;
            }
        }
        return j;
    }

    /*
     * C like strstr function
     */
    function strstr(haystack, needle)
    {
        const l1 = haystack.length;
        const l2 = needle.length;
    
        if (needle === '') {
            return false;
        }
        for (let i = 0; i <= l1 - l2; i++) {
            let j = compare_str(haystack, needle, i, l2);
            if (j === l2) {
                return true;
            }
        }
        return false;
    }

    function is_in_range(q, r)
    {
        q = q.toString();
        for (let i = 0; i < r.length; i++) {
            const r_str = r[i].toString();
            const result = strstr(r_str, q);
            if (result) {
                return true;
            }
        }
        return false;
    }

    /*
     * simulates the range between x and y
     * 1, 4 => [1, 2, 3, 4]
     */
    function create_range(x, y)
    {
        const range = [];

        if (!y || x > y) {
            return range;
        }
        for (let i = x; i <= y; i++) {
            range.push(i);
        }
        return range;
    }

    function format_data(r1, r2, q)
    {
        const r = create_range(str_to_int(r1), str_to_int(r2));

        return is_in_range(str_to_int(q), r);
    }

}
