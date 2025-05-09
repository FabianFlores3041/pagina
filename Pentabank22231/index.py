from flask import Flask, render_template,  request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = 'Robin271.'

def get_db_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=karla\SQLEXPRESS;"  
            "DATABASE=Pentabank;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/inversiones')
def inversiones():
    return render_template('inversiones.html')


@app.route('/cripto')
def cripto():
  
    return render_template("cripto.html")

@app.route('/mercado')
def mercado():
  
  return render_template('mercado.html')


@app.route('/acciones')
def acciones():
  
  return render_template('acciones.html')


@app.route('/materiaprima')
def materiaprima():
  
  return render_template('materiaprima.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')


#-----------------------------SECCION DE Servicios CLIENTES------------------------------------
@app.route('/transacciones_Cli')
def transacciones_Cli():
    return render_template('transacciones.html')

@app.route('/agregarTran', methods=['POST'])
def agregar_transaccion():
    Destinatario = request.form['Destinatario']
    importe = request.form['importe']
    concepto = request.form['concepto']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TransaccionesClientes (Destinatario, importe, concepto) 
        VALUES (?, ?, ?);
    """, (Destinatario, importe, concepto))
    conn.commit()
    conn.close()

    flash("Transferencia realizada con éxito") 

    return redirect(url_for('transacciones_Cli'))

@app.route('/Recargas_cli')
def Recargas_cli():
    return render_template('Recargas.html')

@app.route('/agregarRecar', methods=['POST'])
def agregar_Recarga():
    Para = request.form['Para']
    compania = request.form['compania']     
    importeRe = request.form['importeRe']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO RecargasClientes (Para, compania, importeRe) 
        VALUES (?, ?, ?);
    """, (Para, compania, importeRe))
    conn.commit()
    conn.close()

    flash("Recarga hecha exitosamente")
    return redirect(url_for('Recargas_cli'))

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/luz', methods=['GET', 'POST'])
def luz():
    if request.method == 'POST':
        # Asegúrate de usar .get() para no petar si falta la clave
        Num_Ref  = request.form.get('Num_Ref')
        MontoLuz = request.form.get('MontoLuz')

        # Validación sencilla
        if not Num_Ref or not MontoLuz:
            flash("Debes completar todos los campos", "danger")
            return redirect(url_for('luz'))

        # Inserción en BD
        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ServicioLuz (Num_Ref, MontoLuz) 
            VALUES (?, ?);
        """, (Num_Ref, MontoLuz))
        conn.commit()
        conn.close()

        flash("Luz pagada exitosamente", "success")
        return redirect(url_for('servicios'))

    # Si es GET, muestro el template con el formulario
    return render_template('luz.html')


@app.route('/agua')
def agua():
    return render_template('agua.html')

@app.route('/internet')
def internet():
    return render_template('internet.html')


@app.route('/cuenta')
def cuenta():
    return render_template('cuenta.html')


@app.route('/seguro')
def seguro():
    return render_template('seguro.html')

if __name__ == '__main__':
    app.run(debug=True)
