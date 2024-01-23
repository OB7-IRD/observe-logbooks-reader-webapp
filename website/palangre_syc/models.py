from django.db import models

class common_lightstickstype(models.Model):
    common_lightstickstype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class landing_conservation(models.Model):
    landing_conservation_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_settingshape(models.Model):
    common_settingshape_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_sensordataformat(models.Model):
    observation_sensordataformat_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_hookposition(models.Model):
    observation_hookposition_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_hooksize(models.Model):
    common_hooksize_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_stomachfullness(models.Model):
    observation_stomachfullness_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_sensorbrand(models.Model):
    observation_sensorbrand_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    brandname = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    
    
class common_onboardprocessing(models.Model):
    common_onboardprocessing_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_encountertype(models.Model):
    observation_encountertype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.IntegerField()
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_healthstatus(models.Model):
    common_healthstatus_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_baithaulingstatus(models.Model):
    observation_baithaulingstatus_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_observationmethod(models.Model):
    common_observationmethod_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_itemverticalposition(models.Model):
    observation_itemverticalposition_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_sensortype(models.Model):
    observation_sensortype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_mitigationtype(models.Model):
    common_mitigationtype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.IntegerField()
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_triptype(models.Model):
    common_triptype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_maturitystatus(models.Model):
    observation_maturitystatus_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    uppervalue = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    lowervalue = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_baitsettingstatus(models.Model):
    common_baitsettingstatus_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_baittype(models.Model):
    common_baittype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_catchfate(models.Model):
    common_catchfate_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    observation = models.BooleanField()
    logbook = models.BooleanField()
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_linetype(models.Model):
    common_linetype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class observation_itemhorizontalposition(models.Model):
    observation_itemhorizontalposition_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class landing_datasource(models.Model):
    landing_datasource_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_hooktype(models.Model):
    common_hooktype_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.IntegerField()
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_program(models.Model):
    common_program_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    organism = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    observation = models.BooleanField()
    logbook = models.BooleanField()
    startdate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    status = models.CharField(max_length=100)
    
    
class common_vesselactivity(models.Model):
    common_vesselactivity_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    observation = models.BooleanField()
    logbook = models.BooleanField()
    allowset = models.BooleanField()
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    status = models.CharField(max_length=100)
    
    
class landing_company(models.Model):
    landing_company_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    homeid = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    
    
class common_lightstickscolor(models.Model):
    common_lightstickscolor_id = models.AutoField(primary_key=True)
    topiaid = models.CharField(max_length=100)
    needcomment = models.BooleanField()
    code = models.CharField(max_length=100)
    lastupdatedate = models.CharField(max_length=100)
    topiacreatedate = models.CharField(max_length=100)
    label1 = models.CharField(max_length=100)
    label2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    label3 = models.CharField(max_length=100)
    