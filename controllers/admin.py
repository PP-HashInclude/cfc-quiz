import os
from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
from common import utility, config
from repositories import db, cos

def admin():
    try:
        player_id = session.get("mobileno")
        if player_id is None:
            flash("Please Login as admin.")
            return redirect(request.referrer)

        if player_id != "1000000000":
            flash("Please Login as admin.")
            return redirect(request.referrer)

        if request.method == 'GET':
            return render_template("admin.html")
        elif request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No CSV file selected')
                return redirect(request.url)
            
            if file and utility.allowed_file(file.filename):
                folder_path = config.get("DB_IMPORT", "UPLOAD_FOLDER")
                filename = secure_filename(file.filename)
                file.save(os.path.join(folder_path, filename))

                table_name = request.form.get('tablename')
                isHeader = request.form.get("chkHeader") != None

                isCSVImportOK = db.import_csv_data(folder_path + "/" + filename, table_name, isHeader)
                
                if isCSVImportOK:
                    flash("Data imported successfully")
                    upldmsg = cos.saveCSVFile(filename, folder_path)
                    flash (upldmsg)
                else:
                    flash("Unable to import data..")

                return redirect(request.url)
            else:
                flash("Please select a CSV file")
                return redirect(request.url)
    except Exception as ex:
        print ("Unable to process request..", ex)
    
    return