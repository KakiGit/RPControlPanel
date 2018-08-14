var ws
$.post("ajax/stats.php", function (result) {
    $("#ipaddr").text(result)
    ws = new WebSocket("ws://" + result + ":9011")
    ws.onmessage = function (data) {
        let elements = data.data.split(' ')
        if (elements[0] == '1')
            $(".tip").html(data.data.substr(2))
        else {
            $("#Temperature").text(elements[1] + "℃")
            if (parseInt(elements[1]) >= 60) {
                $("#Temperature").css("background-color", "#d9534f")
                $("#Temperature").css("color", "#ffffff")
            }
            else {
                $("#Temperature").css("background-color", "#ffffff")
                $("#Temperature").css("color", "#000000")
            }
            $("#CPU_Usage").text(elements[2] + "%")
            if (parseInt(elements[2]) >= 80) {
                $("#CPU_Usage").css("background-color", "#d9534f")
                $("#CPU_Usage").css("color", "#ffffff")
            }
            else {
                $("#CPU_Usage").css("background-color", "#ffffff")
                $("#CPU_Usage").css("color", "#000000")
            }
            $("#RAM_Avail").text(elements[3] + "M")
            if (parseInt(elements[3]) <= 200) {
                $("#RAM_Avail").css("background-color", "#d9534f")
                $("#RAM_Usage").css("background-color", "#d9534f")
                $("#RAM_Avail").css("color", "#ffffff")
                $("#RAM_Usage").css("color", "#ffffff")
            }
            else {
                $("#RAM_Avail").css("background-color", "#ffffff")
                $("#RAM_Usage").css("background-color", "#ffffff")
                $("#RAM_Avail").css("color", "#000000")
                $("#RAM_Usage").css("color", "#000000")
            }
            $("#RAM_Usage").text(elements[4] + "%")
            $("#DISK_Avail").text(elements[5] + "G")
            if (parseInt(elements[5]) <= 10) {
                $("#DISK_Avail").css("background-color", "#d9534f")
                $("#DISK_Usage").css("background-color", "#d9534f")
                $("#DISK_Avail").css("color", "#ffffff")
                $("#DISK_Usage").css("color", "#ffffff")
            }
            else {
                $("#DISK_Avail").css("background-color", "#ffffff")
                $("#DISK_Usage").css("background-color", "#ffffff")
                $("#DISK_Avail").css("color", "#000000")
                $("#DISK_Usage").css("color", "#000000")
            }
            $("#DISK_Usage").text(elements[6])
        }
    }
}
)


$(".btn-trigger").click(function () {
    $("#confirm").modal('show')
    let text = $(this).text().replace(/ /g, "").replace(/\n/g, "").replace(/\r/g, "").replace(/\t/g, "")
    let cmd = ""
    switch (text) {
        case "Shutdown":
            cmd = "sudo shutdown -h now"
            break
        case "Reboot":
            cmd = "sudo reboot"
            break
        case "Update":
            cmd = "git pull"
            break
    }
    $("#confirmLabel").text(text)
    $("#confirmBody").text("Do you want to " + text + "?")
    $(".tip").html(cmd)
})

$("#confirmYes").click(function () {
    ws.send($(".tip").html())
    $("#confirm").modal('hide')
})

$("#confirmNo").click(function () {
    $(".tip").html("")
    $("#confirm").modal('hide')
})

$("#GPIO_Panel").click(function () {
    window.open("./sensorHub.html")
})

$("#aria2").click(function () {
    window.open("./webui-aria2/index.html")
})
$("#download").click(function () {
    window.open("./webui-aria2/Downloads/")
})


