<?php
$packet=json_decode('{"device":"desk-01","temperature":29}',true,512,JSON_THROW_ON_ERROR);
if (!isset($packet['temperature']) || !is_numeric($packet['temperature'])) {throw new Exception('缺少温度');}
$result=['device'=>$packet['device'],'command'=>((float)$packet['temperature']>=28?'on':'off')];
echo json_encode($result,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
?>