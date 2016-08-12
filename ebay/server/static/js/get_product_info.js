jQuery(document).ready(function($) {
  // 预加载默认日期
  send_query();
  $('#search').click(function(){
    send_query();
  });

  function send_query() {
    // get parameters
    var start_date = $('#start-date').val();
    var end_date = $('#end-date').val();
    var seller = $('#seller').val();
    var name = $('#name').val();
    var section = $('#section').val();
    // check if start_date is bigger than end_date
    if(start_date > end_date) {
      alert('起始日期必须小于截至日期');
    }
    
    // Ajax POST
    $.ajax({
      url: '/api/info/products',
      type: 'POST',
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        'start_date': start_date,
        'end_date': end_date,
        'seller': seller,
        'name': name,
        'section': section
      })
    })
    .done(function(result) {
      if (result) {
        // buffer for table items
        var _buffer = new Array();
        $.each(result, function (index, product_info) {
          if(price_unit === undefined) {
            var price_unit = product_info['shipping_unit']
          } else {
            var price_unit = product_info['price_unit']
          }
          _buffer.push('<tr>');
          _buffer.push('<td>' + product_info['section'] + '</td>');
          _buffer.push('<td><a href="' + product_info['href'] + '">' + product_info['name'] + '</a></td>');
          _buffer.push('<td><a href="' + product_info['picture'] + '">' + '图片链接</a></td>');
          _buffer.push('<td>' + product_info['create_date'] + '</td>');
          _buffer.push('<td>' + price_unit + '</td>');
          _buffer.push('<td>' + product_info['price'] + '</td>');
          _buffer.push('<td><a href="' + product_info['seller_href'] + '">' + product_info['seller'] + '</a></td>');
          _buffer.push('<td>' + product_info['shipping_unit'] + '</td>');
          _buffer.push('<td>' + product_info['shipping_price'] + '</td>');
          _buffer.push('</tr>');
        });
        
      $('#product_info_table').html(_buffer.join(''));
      }
    });
  }
});
