const button_page_setting = document.querySelector('.button_page_setting')

const button_changeing = document.querySelector('.button_changeing')

const button_product_status = document.querySelector('.button_product_status')

const product_status = document.querySelector('#product_status')

const page_settings = document.querySelector('#page_settings')

const changeing = document.querySelector('#changeing')


let style_page_setting = window.getComputedStyle(page_settings)
let style_changeing = window.getComputedStyle(changeing)
let style_product_status = window.getComputedStyle(product_status)




button_page_setting.addEventListener('click' , () => {
    if(style_changeing.display == 'flex' || style_product_status.display == 'flex'){
        changeing.style.display = 'none'
        product_status.style.display = 'none'
        button_changeing.classList.remove('click_button_profile')
        button_product_status.classList.remove('click_button_profile')
    }
    if(style_page_setting.display == 'none'){
        button_page_setting.classList.add('click_button_profile')
        page_settings.style.display = 'flex'

    }else if(style_page_setting.display == 'flex'){
        button_page_setting.classList.remove('click_button_profile')
        page_settings.style.display = 'none'

    }
})

button_changeing.addEventListener('click' , () => {
    if(style_page_setting.display == 'flex' || style_product_status.display == 'flex'){
        page_settings.style.display = 'none'
        product_status.style.display = 'none'
        button_page_setting.classList.remove('click_button_profile')
        button_product_status.classList.remove('click_button_profile')
    }

    if(style_changeing.display == 'none'){
        button_changeing.classList.add('click_button_profile')
        changeing.style.display = 'flex'

    }else if(style_changeing.display == 'flex'){
        button_changeing.classList.remove('click_button_profile')
        changeing.style.display = 'none'

    }
})


button_product_status.addEventListener('click' , () => {
    if(style_page_setting.display == 'flex' || style_changeing.display == 'flex'){
        page_settings.style.display = 'none'
        changeing.style.display = 'none'
    }

    if(style_product_status.display == 'none'){

        product_status.style.display = 'flex'

    }else if(style_product_status.display == 'flex'){

        product_status.style.display = 'none'

    }
})

