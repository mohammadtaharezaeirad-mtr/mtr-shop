// start add and remove quantity
let quantity_add = document.querySelector('.quantity_add')
let quantity_remove = document.querySelector('.quantity_remove')
let main_quantity =  document.querySelector('.main_quantity')
let main_prce_products = document.querySelector('.main_prce_products')


main_prce_products_number = Number(main_prce_products.innerText)
main_prce_products1 = Number(main_prce_products.innerText)
quantity_add.addEventListener('click' , () => {
    let value_quantity_add = main_quantity.value
    value_quantity_add = Number(value_quantity_add)
    value_quantity_add += 1

    if(main_quantity.value != main_quantity.max){
        main_quantity.value = value_quantity_add
        main_prce_products_number += main_prce_products1
        main_prce_products.textContent = main_prce_products_number

    }
})

quantity_remove.addEventListener('click' , () => {
    let value_quantity_remove = main_quantity.value
    value_quantity_remove = Number(value_quantity_remove)
    value_quantity_remove -= 1
    if(value_quantity_remove != quantity_remove.min){
        main_quantity.value = value_quantity_remove
        main_prce_products_number -= main_prce_products1
        main_prce_products.textContent = main_prce_products_number
    }
})
// end add and remove quantity
