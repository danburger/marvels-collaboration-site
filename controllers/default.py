from datetime import datetime

@auth.requires_login()
def index():
     query = db(db.fielddesign.id>0)
     fielddesign = query.select()
     sort_types = "'String','US','US','US','US','US','String'"
     hide_cols = "[]"
     response.title="Home"
     menu = []
     return dict(layout="table", fielddesign=fielddesign, sort_types=sort_types, hide_cols=hide_cols, menu=menu)

@auth.requires_login()
def targets():
     get_field_id = db.targets(request.args(0)) or redirect(URL('index'))
     targets = db(db.targets.field_id==get_field_id).select()
     sort_types = "'US','String','String','String','String'"
     hide_cols = "[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41]"
     response.title=db(db.fielddesign.id==get_field_id).select().first().field_name + " targets"
     menu = [A('Home', _href='/'+request.application+'/default/index')]
     return dict(layout="table", targets=targets, sort_types=sort_types, hide_cols=hide_cols, menu=menu,)

@auth.requires_login()     
def measurements():
     get_target_id = db.targets(request.args(0)) or redirect(URL('index'))
     measurements = db(db.measurements.target_id==get_target_id).select()
     sort_types = "'String', 'US', 'String', 'String', 'String', 'String'"
     hide_cols = "[]"
     get_field_id=db((db.targets.id==get_target_id) & (db.fielddesign.id==db.targets.field_id)).select().first().fielddesign.id
     get_field_name=db((db.targets.id==get_target_id) & (db.fielddesign.id==db.targets.field_id)).select().first().fielddesign.field_name
     get_target_name=db(db.targets.id==get_target_id).select().first().tyc_name
     if(get_target_name=="NO_TYCHO_STAR_ID"):
         get_target_name=db(db.targets.id==get_target_id).select().first().gsc_name
     response.title=get_target_name + " measurements"
     options = A('Add new measurement', _href=URL('new_measurements', args=request.args(0)))
     menu = [A('Home', _href='/'+request.application+'/default/index'), A(get_field_name, _href='/'+request.application+'/default/targets/'+str(get_field_id))]
     properties = db().select(db.measurements_properties.ALL)
     units = db().select(db.measurements_units.ALL)
     sources = db().select(db.measurements_sources.ALL)
     return dict(layout="table", measurements=measurements, sort_types=sort_types, hide_cols=hide_cols, menu=menu, options=options, properties=properties, units=units, sources=sources)

@auth.requires_login()
def new_measurements():
     get_target_id = db.targets(request.args(0)) or redirect(URL('index'))
     get_field_id=db((db.targets.id==get_target_id) & (db.fielddesign.id==db.targets.field_id)).select().first().fielddesign.id
     get_field_name=db((db.targets.id==get_target_id) & (db.fielddesign.id==db.targets.field_id)).select().first().fielddesign.field_name
     get_target_name=db(db.targets.id==get_target_id).select().first().tyc_name
     if(get_target_name=="NO_TYCHO_STAR_ID"):
         get_target_name=db(db.targets.id==get_target_id).select().first().gsc_name
     response.title="New measurement"
     menu = [A('Home', _href='/'+request.application+'/default/index'), A(get_field_name, _href='/'+request.application+'/default/targets/'+str(get_field_id)), A(get_target_name, _href='/'+request.application+'/default/measurements/'+str(get_target_id.id))]

     form = SQLFORM(db.measurements, fields=['property', 'value', 'units', 'source', 'measured_by', 'timestamp_taken'])
     property_form = SQLFORM(db.measurements_properties)
     source_form = SQLFORM(db.measurements_sources)
     form.vars.target_id = get_target_id
     form.vars.created_by=auth.user.first_name+" "+auth.user.last_name
     form.vars.timestamp_created=datetime.now()
     form.vars.modified_by=auth.user.first_name+" "+auth.user.last_name
     form.vars.timestamp_modified=datetime.now()
     
     if form.accepts(request.vars, session, dbio=False, onvalidation=validate_measurements):
         if form.vars.property == '1':
             new_property = db.measurements_properties.insert(property_name=request.vars.property_name.strip())
             form.vars.property = new_property
         if form.vars.source == '1':
             new_source = db.measurements_sources.insert(source_name=request.vars.source_name.strip())
             response.flash = request.vars.source_name
             form.vars.source = new_source
         form.vars.id = db.measurements.insert(**dict(form.vars))
         redirect(URL('measurements/'+request.args(0)))
     elif form.errors:
         response.flash = 'form has errors'
     else:
         response.flash = 'please fill out the form'
     return dict(layout="form", form=form, property_form=property_form, source_form=source_form, menu=menu)
     
@auth.requires_login()
def validate_measurements(form):
     print "Hi there!"
     if request.vars.property == '1' and request.vars.property_name.strip() == '':
         form.errors.property = 'Please name the new property below.'
     if request.vars.source == '1' and request.vars.source_name.strip() == '':
         form.errors.source = 'Please name the new source below.'

@auth.requires_login()
def edit_measurements():
     get_measurement_id = db.measurements(request.args(0)) or redirect(URL('index'))
     get_target_id = db((db.measurements.id==get_measurement_id) & (db.targets.id==db.measurements.target_id)).select().first().targets.id
     get_measurement_name = db.measurements_properties[get_measurement_id.property].property_name
     get_field_id=db((db.targets.id==get_target_id) & (db.fielddesign.id==db.targets.field_id)).select().first().fielddesign.id
     get_field_name=db((db.targets.id==get_target_id) & (db.fielddesign.id==db.targets.field_id)).select().first().fielddesign.field_name
     get_target_name=db(db.targets.id==get_target_id).select().first().tyc_name
     if(get_target_name=="NO_TYCHO_STAR_ID"):
         get_target_name=db(db.targets.id==get_target_id).select().first().gsc_name
     response.title="Edit "+get_measurement_name+" measurement"
     menu = [A('Home', _href='/'+request.application+'/default/index'), A(get_field_name, _href='/'+request.application+'/default/targets/'+str(get_field_id)), A(get_target_name, _href='/'+request.application+'/default/measurements/'+str(get_target_id))]
     
     get_meas_id = db.measurements(request.args(0)) or redirect(URL('index'))
     form = SQLFORM(db.measurements, get_meas_id, fields=['property', 'value', 'units', 'source', 'measured_by', 'timestamp_taken'])
     property_form = SQLFORM(db.measurements_properties)
     source_form = SQLFORM(db.measurements_sources)
     form.vars.modified_by=auth.user.first_name+" "+auth.user.last_name
     form.vars.timestamp_modified=datetime.now()
     
     if form.accepts(request.vars, session, dbio=False, onvalidation=validate_measurements):
         if form.vars.property == '1':
             new_property = db.measurements_properties.insert(property_name=request.vars.property_name.strip())
             form.vars.property = new_property
         if form.vars.source == '1':
             new_source = db.measurements_sources.insert(source_name=request.vars.source_name.strip())
             response.flash = request.vars.source_name
             form.vars.source = new_source
         get_meas_id.update_record(**dict(form.vars))
         redirect(URL('measurements/'+str(get_target_id)))
     elif form.errors:
         response.flash = 'form has errors'
     else:
         response.flash = 'please fill out the form'
     return dict(layout="form", form=form, property_form=property_form, source_form=source_form, menu=menu)

def user(): 
    if(auth.is_logged_in()):
        menu = [A('Home', _href='/'+request.application+'/default/index')]
    else:
        menu = []
    return dict(layout="none", form=auth(), menu=menu)

def registration_submitted(): return dict(layout="none", menu=[])

@auth.requires_login()
def user_list():
     try:
         if(auth.has_membership('admin') and request.args[0]=='make_admin'):
             auth.add_membership(auth.id_group('admin'),request.args[1])
             selected_user = db(db.auth_user.id==request.args[1]).select().first()
             response.flash=selected_user.first_name + " " + selected_user.last_name + " is now an administrator."
         if(auth.has_membership('admin') and request.args[0]=='revoke_admin'):
             auth.del_membership(auth.id_group('admin'),request.args[1])
             selected_user = db(db.auth_user.id==request.args[1]).select().first()
             response.flash=selected_user.first_name + " " + selected_user.last_name + " is no longer an administrator."
         if(auth.has_membership('admin') and request.args[0]=='block'):
             db(db.auth_user.id==request.args[1]).update(registration_key = "blocked")
             selected_user = db(db.auth_user.id==request.args[1]).select().first()
             response.flash=selected_user.first_name + " " + selected_user.last_name + " is now blocked from the site."
         if(auth.has_membership('admin') and request.args[0]=='unblock'):
             db(db.auth_user.id==request.args[1]).update(registration_key = "")
             selected_user = db(db.auth_user.id==request.args[1]).select().first()
             response.flash=selected_user.first_name + " " + selected_user.last_name + " is no longer blocked from the site."
     except:pass
     query = db(db.auth_user.registration_key=="")
     if(auth.has_membership('admin')):
          query = db(db.auth_user.id>0)
     users = query.select()
     sort_types = ""
     hide_cols = "[]"
     response.title="User list"
     menu = [A('Home', _href='/'+request.application+'/default/index')]
     return dict(layout="table", users=users, sort_types=sort_types, hide_cols=hide_cols, menu=menu)

@auth.requires_membership('admin')
def approve_users():
     try:
         if(request.args[0]=='approve'):
             db(db.auth_user.id==request.args[1]).update(registration_key = "")
             new_user = db(db.auth_user.id==request.args[1]).select().first()
             notify_new_user(new_user)
             response.flash=new_user.first_name + " " + new_user.last_name + " has been approved. An e-mail notification has been sent to the new user."
         if(request.args[0]=='deny'):
             db(db.auth_user.id==request.args[1]).update(registration_key = "blocked")
             new_user = db(db.auth_user.id==request.args[1]).select().first()
             response.flash=new_user.first_name + " " + new_user.last_name + " is now blocked from the site."
     except:pass
     query = db(db.auth_user.registration_key=='pending')
     users = query.select()
     sort_types = ""
     hide_cols = "[]"
     response.title="Approve users"
     menu = [A('Home', _href='/'+request.application+'/default/index')]
     return dict(layout="table", users=users, sort_types=sort_types, hide_cols=hide_cols, menu=menu)

@auth.requires_membership('admin')
def edit_user():
     get_user_id = db.auth_user(request.args(0)) or redirect(URL('index'))
     form = SQLFORM(db.auth_user, get_user_id, fields=['first_name','last_name','role','institutional_affiliation','city','state_or_province','country','email'])
     if form.accepts(request.vars, session):
         response.flash = 'The user information has been updated.'
     elif form.errors:
         response.flash = 'form has errors'
     else:
         response.flash = 'please fill out the form'
     response.title="Edit user"
     menu = [A('Home', _href='/'+request.application+'/default/index'), A('User list', _href='/'+request.application+'/default/user_list')]
     return dict(layout="form", form=form, menu=menu)
