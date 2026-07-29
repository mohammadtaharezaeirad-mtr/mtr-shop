let quantity_adds = document.querySelectorAll('.quantity_add');
let quantity_removes = document.querySelectorAll('.quantity_remove');
let main_quantitys = document.querySelectorAll('.main_quantity');
let main_prce_products = document.querySelectorAll('.main_prce_products');
let submit_quantity = document.querySelectorAll('#submit_quantity')

main_quantitys.forEach((main_quantity , index) => {
    let main_quantity_p = Number(main_quantity.value)
    let main_prce_product_p = Number(main_prce_products[index].innerText)
    if(main_quantity.value > 1){
        main_prce_products[index].textContent = main_prce_product_p * main_quantity_p
    }

})

quantity_adds.forEach((quantity_add, index) => {

    let main_quantity = main_quantitys[index];
    let main_prce_product = main_prce_products[index];

    let unitPrice = Number(main_prce_product.textContent.replace(/,/g, ""));

    quantity_add.addEventListener("click", () => {
        
        let quantity = Number(main_quantity.value);

        if (quantity < Number(main_quantity.max)) {

            quantity++;
            main_quantity.value = quantity;

            
            main_prce_product.textContent = (unitPrice * quantity).toLocaleString();
        }
        submit_quantity[index].click()
    });
});




quantity_removes.forEach((quantity_remove, index) => {

    let main_quantity = main_quantitys[index];
    let main_prce_product = main_prce_products[index];

    let unitPrice = Number(main_prce_product.textContent.replace(/,/g, ""));

    quantity_remove.addEventListener("click", () => {

        let quantity = Number(main_quantity.value);

        if (quantity > 1) {

            quantity--;
            main_quantity.value = quantity;

            main_prce_product.textContent = (unitPrice * quantity).toLocaleString();
            
            submit_quantity[index].click()
        }

    });

});

//start separating three by three product prices
main_prce_products.forEach((p) => {
    let prce_products_number = Number(p.innerText)
    p.textContent = prce_products_number.toLocaleString()
})

//end separating three by three product prices 