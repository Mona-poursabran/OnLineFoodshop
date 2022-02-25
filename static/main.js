window.onload = function (){

const url=  window.location.href
const searchForm = document.getElementById("search-form")
const searchInput = document.getElementById("search-input")
const resultBox = document.getElementById('result-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (data)=>{
    $.ajax({
        type:'POST',
        url: URL,
        data :{
            'csrfmiddlewaretoken':csrf,
            'data': data,
        },
        success: function(res){
            // console.log(res.dataa)
            const data = res.dataa
            if (Array.isArray(data)){
                resultBox.innerHTML = ''
                data.forEach(food=>{
                    resultBox.innerHTML += `
                    
                    <a href="${url}${food.pk}" class='item' >
                        <div class ="row" style="margin-left:10px">
                            <div class ="col-2>
                                <p class="text-muted" ><img src="${food.food.img}" class="food-img"> 
                                <b style="color:black">${food.food.food_name}</b><b style="color:#17a2b8">
                                ${food.menu.name}</b> <b style="color:#6610f2">${food.price} ${food.menu.branch}
                                </b></p>
                            </div>
                        </div>
                    </a>
                    `
                })


            }else{
                if (searchInput.value.length > 0){
                    resultBox.innerHTML=`<b>${data}</b>`
                }else{
                    resultBox.classList.add('not-visible')
                }
            }
       
        },
        error: function(error){
            console.log(error)
        }
    })
}


// load whatever is added in search input as value (letter by letter)
searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)
    if (resultBox.classList.contains('not-visible')){
        resultBox.classList.remove('not-visible')
    }
    sendSearchData(e.target.value)
    
})
 
  
}