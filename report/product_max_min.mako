<html dir="rtl" lang="ar">
<head>
    <meta charset="utf-8">
</head>
<body>
<div align="center">


% for product in objects:
<h1><bdi>أسم المنتج:</bdi> <bdi> ${product.name|entity}</bdi></h1>
    <small> <bdi> كود المنتج:</bdi>  <bdi>${product.code|entity}</bdi></small>
    <br>
    <hr>
    </div>
    <h2> <bdi>حالته:</bdi>
    % if product.quantity > product.max:
        <bdi>زايد</bdi>
    % elif product.quantity <= product.min:
        <bdi> ناقص</bdi>
       % else :
        <bdi> لا توجد زياده اونقصان</bdi>
    </h2>
    % endif
<h4><bdi> فى المخزن: </bdi> <bdi> ${product.warehouse_id.name} </bdi></h4>
%endfor




</body>

</html>

