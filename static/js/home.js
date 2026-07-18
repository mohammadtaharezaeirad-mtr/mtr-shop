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