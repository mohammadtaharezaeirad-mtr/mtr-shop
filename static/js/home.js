// start slider
const slider = document.querySelector('#main_slider')

let trans = 0
setInterval(() => {
    if(trans == 0){
        trans = 100
        slider.style.transform = 'translateX(100%)';
    }else if(trans == 100){
        trans = 200
        slider.style.transform = 'translateX(200%)';
    }else if(trans == 200){
        trans = 0
        slider.style.transform = 'translateX(0%)';
    }


},4000)
//end slider

//start main products
const main_products = document.querySelector('#main_products')
const btn_right_view = document.querySelector('#btn_right_view')
const btn_left_view = document.querySelector('#btn_left_view')

let trans_btn_right_left = 10
btn_right_view.addEventListener('click', () => {
    if(trans_btn_right_left != 100){
    trans_btn_right_left += 10
    main_products.style.transform = `translateX(${trans_btn_right_left}%)`
    }
})

btn_left_view.addEventListener('click' , () => {
    if(trans_btn_right_left  != -100){
    trans_btn_right_left -= 10
    main_products.style.transform = `translateX(${trans_btn_right_left}%)`
    }
})
//end main products