itemVisibleState = true;

function toggleAllItems() {
    $(".toggleall").each(function() {
        if (itemVisibleState === true) {
            $(this).hide("medium");
        } else {
            $(this).show("medium");
        }
    });
    if (itemVisibleState === true) {
        itemVisibleState = false;
        console.log(itemVisibleState);
    } else {
        itemVisibleState = true;
        console.log(itemVisibleState);
    }
}
