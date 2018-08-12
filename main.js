var ws
$.ajax({
    type: "POST",
    url: "ajax/stats.php",
    success: function (result) {
        $("#ipaddr").text(result)
        ws = new WebSocket("ws://" + result + ":9011")
        ws.onmessage = function (data) {
            console.log(data)
            let elements = data.data.split(' ')
            $("#Temperature").text(elements[0] + "℃")
            if (parseInt(elements[0]) >= 60) {
                $("#Temperature").css("background-color", "#d9534f")
                $("#Temperature").css("color", "#ffffff")
            }
            else {
                $("#Temperature").css("background-color", "#ffffff")
                $("#Temperature").css("color", "#000000")
            }
            $("#CPU_Usage").text(elements[1] + "%")
            if (parseInt(elements[1]) >= 80) {
                $("#CPU_Usage").css("background-color", "#d9534f")
                $("#CPU_Usage").css("color", "#ffffff")
            }
            else {
                $("#CPU_Usage").css("background-color", "#ffffff")
                $("#CPU_Usage").css("color", "#000000")
            }
            $("#RAM_Avail").text(elements[2] + "M")
            if (parseInt(elements[2]) <= 200) {
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
            $("#RAM_Usage").text(elements[3] + "%")
            $("#DISK_Avail").text(elements[4] + "G")
            if (parseInt(elements[4]) <= 10) {
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
            $("#DISK_Usage").text(elements[5])
        }
    }
})

$(function () {
    $(".btn-trigger").click(function () {
        let text = $(this).text().replace(/ /g, "").replace(/\n/g, "").replace(/\r/g, "").replace(/\t/g, "")
        let cmd = ""
        switch (text) {
            case "关机":
                cmd = "sudo shutdown -h now"
                break
            case "重启":
                cmd = "sudo reboot"
                break
        }
        if (confirm("确定要执行该命令吗？")) {
            ws.send(cmd)
        }
    })
})

$(function () {
    $("#aria2").click(function () {
        window.open("./webui-aria2/index.html")
    })
    $("#download").click(function () {
        window.open("./webui-aria2/Downloads/")
    })
})

