/* $('#toggleitem{{c.id}}').slideToggle();
$("[id^=main]")
*/

function toggleAllItems() {
    $(".toggleall").each(function() {
        console.log(this);
        $(this).toggle();
    });
}

function Filter(filterstring) {
    console.log(filterstring);
}
