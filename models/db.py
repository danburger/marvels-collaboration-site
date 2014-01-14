db = None;
if request.application == "marvelsdev":
    db = DAL('mysql://marvelsdevuser:ndsle4!@localhost/marvelsdev')
else:
    db = DAL('mysql://burgerdm:ndsle4!@localhost/marvels')

from gluon.tools import Auth
auth = Auth(globals(), db)

db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('role', length=128, default=''),
    Field('institutional_affiliation', length=128, default=''),
    Field('city', length=128, default=''),
    Field('state_or_province', length=128, default=''),
    Field('country', length=128, default=''),
    Field('email', length=128, default='', unique=True),
    Field('password', 'password', length=512,
          readable=False, label='Password'),
    Field('registration_key', length=512,
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,
          writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(min=7, special=0, upper=0), CRYPT()]
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]
auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table

from gluon.tools import Mail
mail = Mail(globals())
mail.settings.server = 'smtp.gmail.com:587'
#mail.settings.server = 'logging'
mail.settings.sender = 'marvels.data@gmail.com'
mail.settings.login = 'marvels.data:m4rv3l5Pr0j'
auth.settings.mailer = mail
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
#auth.messages.verify_email = 'Click on the link http://delia.phy.vanderbilt.edu/marvels/default/user/verify_email' + \
#    '/%(key)s to verify your email'
auth.messages.reset_password = 'Click on the link http://delia.phy.vanderbilt.edu/'+request.application+'/default/user/reset_password' + '/%(key)s to reset your password'

auth.settings.register_next = URL('registration_submitted', args='Registration submitted')

def mail_all_admins(form):
    mail.send(to=form.vars.email, subject='Your registration has been submitted for approval', message=form.vars.first_name+":\n\nThis e-mail is to confirm your registration for the MARVELS collaboration site at http://delia.phy.vanderbilt.edu/"+request.application+". Your registration will be sent to the administrators for approval. If you do not receive a response within 48 hours, please let us know.\n\nThanks,\nThe MARVELS Site Administration Team\nmarvels.data@gmail.com")
    admin_list = []
    for person in db(db.auth_user.id>0).select():
        if(auth.has_membership(None,person.id,'admin')):
            admin_list.append(person.email)
    mail.send(to=admin_list, subject=form.vars.first_name+' '+form.vars.last_name+' is waiting for approval on the MARVELS collaboration site', message=form.vars.first_name+' '+form.vars.last_name+' ('+form.vars.email+') is waiting for approval on the MARVELS collaboration site. Please go to http://delia.phy.vanderbilt.edu/'+request.application+'/default/approve_users/ to respond to this registration.')

def notify_new_user(new_user):
     mail.send(to=new_user.email, subject='Your registration has been approved', message=new_user.first_name+":\n\nYour registration for the MARVELS collaboration site has been approved. You may now log in to the collaboration page at http://delia.phy.vanderbilt.edu/"+request.application+". If you have any problems logging in, please let us know.\n\nThanks,\nThe MARVELS Site Administration Team\nmarvels.data@gmail.com")

auth.settings.register_onaccept.append(lambda form: mail_all_admins(form))

auth.define_tables(username=False)

db.define_table('fielddesign',
    Field('field_name', 'string', length=100),
    Field('number_of_targets', 'integer'),
    Field('number_of_good_targets', 'integer'),
    Field('faintest_target','double'),
    Field('plate_center_ra','double'),
    Field('plate_center_dec','double'),
    migrate=False,fake_migrate=True)
    
db.define_table('targets',
    Field('field_id', 'integer'),
    Field('target_number', 'integer'),
    Field('gsc_name', 'string', length=15),
    Field('tyc_name', 'string', length=16),
    Field('hip_name', 'string', length=9),
    Field('twomass_name', 'string', length=23),
    Field('final_ra_deg', 'double'),
    Field('final_dec_deg', 'double'),
    Field('gsc_b_mag', 'double'),
    Field('gsc_v_mag', 'double'),
    Field('twomass_j_mag', 'double'),
    Field('twomass_h_mag', 'double'),
    Field('twomass_k_mag', 'double'),
    Field('sp_type_1', 'string', length=3),
    Field('sp_type_2', 'string', length=3),
    Field('lumin_class', 'string', length=7),
    Field('teff', 'double'),
    Field('log_g', 'double'),
    Field('fe_h', 'double'),
    Field('gsc_b_mag_err', 'double'),
    Field('gsc_v_mag_err', 'double'),
    Field('twomass_j_mag_err', 'double'),
    Field('twomass_h_mag_err', 'double'),
    Field('twomass_k_mag_err', 'double'),
    Field('teff_err', 'double'),
    Field('log_g_err', 'double'),
    Field('fe_h_err', 'double'),
    Field('epoch_zero_deg', 'double'),
    Field('ra_zero_deg', 'double'),
    Field('dec_zero_deg', 'double'),
    Field('twomass_ra_deg', 'double'),
    Field('twomass_dec_deg', 'double'),
    Field('gsc_pm_ra', 'double'),
    Field('gsc_pm_dec', 'double'),
    Field('gsc_pm_ra_err', 'double'),
    Field('gsc_pm_dec_err', 'double'),
    Field('tyc_b_mag', 'double'),
    Field('tyc_v_mag', 'double'),
    Field('tyc_b_mag_err', 'double'),
    Field('tyc_v_mag_err', 'double'),
    Field('hip_plx', 'double'),
    Field('hip_plx_err', 'double'),
    Field('hip_sp_type', 'string', length=12),
    migrate=False,fake_migrate=True)
    
db.define_table('measurements_properties',
    Field('property_name', 'string', length=100, requires=IS_NOT_EMPTY()),
    format='%(property_name)s')

db.define_table('measurements_units',
    Field('unit_name', 'string', length=100),
    format='%(unit_name)s')
    
db.define_table('measurements_sources',
    Field('source_name', 'string', length=100),
    format='%(source_name)s')
    
db.define_table('measurements',
    Field('target_id', 'integer'),
    Field('property', db.measurements_properties),
    Field('value', 'string', length=100),
    Field('units', db.measurements_units),
    Field('source', db.measurements_sources),
    Field('measured_by', 'string', length=100),#, default=auth.user.first_name+" "+auth.user.last_name),
    Field('timestamp_taken', 'datetime'),
    Field('created_by', 'string', length=100),
    Field('timestamp_created', 'datetime'),
    Field('modified_by', 'string', length=100),
    Field('timestamp_modified', 'datetime'))
db.measurements.property.requires = IS_IN_DB(db, 'measurements_properties.id', '%(property_name)s', zero=T('Select a property'))
db.measurements.units.requires = IS_IN_DB(db, 'measurements_units.id', '%(unit_name)s', zero=T('Select units'))
db.measurements.source.requires = IS_IN_DB(db, 'measurements_sources.id', '%(source_name)s', zero=T('Select a source'))
