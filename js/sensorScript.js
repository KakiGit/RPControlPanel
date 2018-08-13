
// $('#GPIO_0_Mode').click(function () {
//     if ($(this).prop('checked'))
//         $('#GPIO_0_PWM').removeClass("d-none")
//     else
//         $('#GPIO_0_PWM').addClass("d-none")
// })
// let GPIOs = ['0', '1']

let GPIOs = ['0', '1', '2', '3', '4', '5', '6', '7', '21', '22', '23', '24', '25', '26', '27', '28', '29']


for (let x in GPIOs) {
    let i = GPIOs[x]
    $('#GPIO_' + i + '_Mode').click(function () {
        console.log(i)
        if ($(this).prop('checked'))
            $('#GPIO_' + i + '_PWM').removeClass("d-none")
        else
            $('#GPIO_' + i + '_PWM').addClass("d-none")
    })
}
