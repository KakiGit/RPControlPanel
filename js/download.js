

$(function () {
    $.contextMenu({
        selector: '.btn',
        callback: function (key, options) {
            var m = "clicked: " + key;
            console.log(m);
        },
        items: {
            "download": { name: "Download" },
            "delete": { name: "Delete" },
        }
    });

})
