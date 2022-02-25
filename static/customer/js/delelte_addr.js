
function deleteAddress(id){
    if (confirm("Are you sure?")){
      $.ajax({
        url = "{% url 'delete_addr' %}",
        data :{
          'id': id
        },
        dataType :"json",
        success : function(data){
          if (data.deleted){
            $("#AddrTable  #address-" + id ).remove()
            location.reload()
          }
        }
      });
     
    }
  }


  function updateToAddrTable(address){
    $("#AddrTable #address-" + address.id).children(".userDate").each(function(){
      var attr = $(this).attr("city");
          if (attr == "city") {
            $(this).text(address.city);
          } else if (attr == "street") {
            $(this).text(address.street);
          } else {
            $(this).text(address.plaque);
          }
    });
  };
  

  function editAddress(id){
    if (id){
      tr_id = "#address-"+id;
      city = $(tr_id).find(".AddressCity").text();
      street = $(tr_id).find(".AddressStreet").text();
      plaque = $(tr_id).find(".AddressPlaque").text();
  
      $("#form-id").val(id);
      $('#form-city').val(city);
      $('#form-street').val(street);
      $('#form-plaque').val(plaque);
    }
  };
  

  $("form#updateAddress").submit(function(){
    var idInput = $('input[name= "formId"]').val().trim();
    var cityInput = $('input[name = "formCity"]').val().trim();
    var streetInput = $('input[name= "formStreet"]').val().trim();
    var plaquetInput = $('input[name= "formPlaque"]').val().trim();
  
    if (cityInput && streetInput && plaquetInput){
      $.ajax({
        url : '{% url "update_addr" %}',
        data :{
          'id': idInput,
          'city': cityInput,
          'street': streetInput,
          'plaque': plaquetInput
        },
        dataType : "jason",
        success : function(data){
            if (data.address){
              updateToAddrTable(data.address)
            }
        }
      });
    }else{
      alert("All fields must have a valid value!")
    }
    $('form#updateAddress').trigger("reset");
    $('#myModel').model('hide');
    return false;
  
  });


  

$('form#addAddress').submit(function(event){
    event.preventDefault();
  
    var cityInput = $('input[name = "city"]').val().trim();
    var streetInput = $('input[name= "street"]').val().trim();
    var plaquetInput = $('input[name= "plaque"]').val();
    console.log(cityInput)
    console.log(streetInput)
    console.log(plaquetInput)
  
  
    if (cityInput && streetInput && plaquetInput){
      console.log("Yessssss")
        $.ajax({
            url : '{% url "create_addr" %}',
            data :{ 
                'city': cityInput,
                'street': streetInput,
                'plaque' : plaquetInput
            },
            dataType : "json",
            success : function(data){
                if (data.address){
                    appendToAddrTable(data.address)
                }
            }
        });
  
        }else{
          alert("All Fields must have a valid value!");
        }
        $('form#addAddress').trigger("reset");
        return false;
  });
  
  
  function appendToAddrTable(address){
    console.log(address, "addressssss")
    $('#AddrTable > tbody:last-child').append(`
    <tr id="address-${addr.address.id}">
        <td class="AddressCity" name="city"> ${address.city}</td>
        <td class= "AddressStreet name="street"> ${address.street} </td>
        <td class="Addressplaque" name="plaque"> ${address.plaque} </td>
        <td align="center">
          <button class="btn btn-success form-control" onClick="editAddress(${address.id})" data-toggle="modal" data-target="#myModal")">EDIT</button>
      </td>
      <td align="center">
          <button class="btn btn-danger form-control" onClick="deleteAddress(${address.id})">DELETE</button>
      </td>
  </tr> 
    `)
  };
  


  