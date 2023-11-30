  function payWithPayStack(){
   let currency = "GHS";
   let plan = "";
   let ref = "{{ payment.ref }}"
   let obj = {
       key: '{{ paystack_public_key }}',
       email: '{{ payment.email }}',
       amount: '10',
    //    amount: '{{ payment.amount_value }}',
       ref: ref,
       callback: function(response){
           window.location.href = "{% url 'payment:verify-payment' payment.ref %}";
       }
   }
   if (Boolean(currency)) {
       obj.currency = currency.toUpperCase
   }
   if (Boolean(plan)){
       obj.plan = plan;
   }
   var handler = PaystackPop.setup(obj);
   handler.openIframe();
  }
