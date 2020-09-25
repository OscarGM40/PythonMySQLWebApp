const btnDelete = document.getElementsByClassName('actiondelete');

if(btnDelete) {
    const btnArray = Array.from(btnDelete)

    btnArray.forEach((btn)=>{
        btn.addEventListener('click',(e)=>{
            if(!confirm('Are you sure you want to delete this contact')){
                e.preventDefault();
            }
        })
    })
}

ScrollReveal().reveal('.navbar',{
    duration:1500,
    distance:'150px',
    origin:'bottom',
    
})

ScrollReveal().reveal('.row',{
    duration:1500,
    distance:'150px',
    origin:'right'
})