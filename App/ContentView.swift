import SwiftUI

// PANTALLA: recoge las entradas y muestra el resultado que devuelve el modelo.
// Aquí no escribimos las fórmulas de la boleta; llamamos a la clase Boleta.
struct ContentView: View {
    // @State guarda datos que pueden cambiar mientras se usa la pantalla.
    // Cuando cambia uno de ellos, SwiftUI actualiza las partes que lo muestran.
    // Los TextField guardan String (texto), aunque la persona escriba números.
    // Los convertimos a Decimal o Int al pulsar Calcular, para poder validarlos.
    @State private var sueldo = "2500"
    @State private var dias = "30"
    @State private var hijos = false
    @State private var sistema = Sistema.onp
    @State private var afp = "Ejemplo"
    @State private var horas25 = "0"
    @State private var horas35 = "0"
    @State private var adelantos = "0"
    // El signo ? permite que resultado sea nil: todavía no existe una boleta.
    // Los valores iniciales del formulario corresponden al caso 1 de la guía.
    @State private var resultado: ResultadoBoleta?
    // error guarda el mensaje de validación; descripcion resume los datos usados
    // en el último cálculo, incluso si después se edita otra vez el formulario.
    @State private var error = ""
    @State private var descripcion = ""

    var body: some View {
        // ScrollView permite desplazar el formulario y el resultado en un celular.
        ScrollView {
            // VStack coloca los controles uno debajo del otro.
            VStack(alignment: .leading, spacing: 18) {
                Text("Boleta de ejemplo").font(.largeTitle).bold()
                Text("Semana 9 · Del sueldo al neto").foregroundStyle(.secondary)
                Text("Perfil de la guía: RMV S/ 1,230. AFP Ejemplo usa tasas de prueba. Sin renta de quinta categoría.")
                    .font(.footnote)
                Text("Datos del mes").font(.title2).bold()
                // El símbolo $ crea una conexión de lectura y escritura (Binding):
                // lo que se escribe en el campo actualiza la variable sueldo.
                campo("Sueldo básico (S/)", texto: $sueldo)
                VStack(alignment: .leading) {
                    Text("Días laborados (1–30)")
                    TextField("30", text: $dias).keyboardType(.numberPad).textFieldStyle(.roundedBorder)
                }
                // tag relaciona cada etiqueta visible con el valor que se guarda:
                // No guarda false y Sí guarda true. No se pide cantidad de hijos.
                Picker("¿Tiene hijos?", selection: $hijos) {
                    Text("No").tag(false)
                    Text("Sí").tag(true)
                }.pickerStyle(.segmented)
                Text("Sistema de pensiones")
                Picker("Sistema de pensiones", selection: $sistema) {
                    Text("ONP").tag(Sistema.onp)
                    Text("AFP").tag(Sistema.afp)
                }.pickerStyle(.segmented)
                // Este if muestra el selector de AFP únicamente cuando corresponde.
                // ONP y AFP son alternativas; no se descuentan las dos a la vez.
                if sistema == .afp {
                    Picker("AFP", selection: $afp) {
                        Text("Ejemplo").tag("Ejemplo")
                        Text("Habitat (flujo)").tag("Habitat (flujo)")
                        Text("Integra (flujo)").tag("Integra (flujo)")
                        Text("Prima (flujo)").tag("Prima (flujo)")
                        Text("Profuturo (flujo)").tag("Profuturo (flujo)")
                    }.pickerStyle(.menu)
                    Text("AFP reales: tasas de flujo SBS consultadas el 26/10/2026; se aplica la simplificación de la guía.").font(.footnote)
                }
                campo("Horas extras al 25%", texto: $horas25)
                campo("Horas extras al 35%", texto: $horas35)
                campo("Adelantos (S/)", texto: $adelantos)
                Text("Usa punto o coma decimal, sin miles. Completa con 0 los campos que no aplican.").font(.footnote)
                // Pulsar el botón ejecuta la función calcular() del final del archivo.
                Button("Calcular") { calcular() }.buttonStyle(.borderedProminent)
                // Si hay un error, mostramos su explicación en la misma pantalla.
                if !error.isEmpty { Text(error).foregroundStyle(.red).accessibilityLabel("Error: \(error)") }
                // if let comprueba que exista un resultado y lo llama b dentro
                // de este bloque. Así no mostramos una boleta antes de calcular.
                if let b = resultado {
                    Text("Resultado del último cálculo").font(.title2).bold()
                    Text(descripcion).font(.footnote)
                    // Los arrays del modelo se presentan en los tres bloques pedidos.
                    // Dinero.texto prepara los montos para leerlos con dos decimales.
                    bloque("REMUNERACIONES", conceptos: b.remuneraciones)
                    fila("Total remuneraciones", b.totalRemuneraciones).bold()
                    bloque("RETENCIONES / DESCUENTOS", conceptos: b.descuentos)
                    fila("Total descuentos", b.totalDescuentos).bold()
                    bloque("APORTACIONES DEL EMPLEADOR", conceptos: b.aportaciones)
                    Text("EsSalud lo paga la empresa; no reduce tu neto.").font(.footnote)
                    Text("NETO A PAGAR: S/ \(Dinero.texto(b.neto))").font(.title2).bold().foregroundStyle(.blue)
                    if b.neto < 0 { Text("Los descuentos superan las remuneraciones; revisa el adelanto.").foregroundStyle(.red) }
                }
            }.padding()
        }
    }

    // Reutilizamos esta función para no repetir la etiqueta y el campo decimal.
    // Binding<String> permite que cada campo edite la variable que recibió con $.
    // El teclado decimal facilita escribir, pero la validación la hace el modelo.
    private func campo(_ titulo: String, texto: Binding<String>) -> some View {
        VStack(alignment: .leading) {
            Text(titulo)
            TextField("0", text: texto).keyboardType(.decimalPad).textFieldStyle(.roundedBorder)
        }
    }
    // HStack coloca el nombre y el importe en la misma fila, de izquierda a derecha.
    // monospacedDigit alinea mejor los números; no modifica el cálculo del monto.
    private func fila(_ nombre: String, _ monto: Decimal) -> some View {
        HStack {
            Text(nombre).frame(maxWidth: .infinity, alignment: .leading)
            Text("S/ \(Dinero.texto(monto))").monospacedDigit()
        }
    }
    // Se escriben las filas explícitamente para respetar los controles vistos en clase.
    // Un array se recorre aquí por posiciones: [0] es la primera, [1] la segunda.
    // Antes de leer cada posición comprobamos count para no acceder fuera del array.
    // Los bloques pueden tener 4 remuneraciones, 5 descuentos o 1 aporte.
    private func bloque(_ titulo: String, conceptos: [Concepto]) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(titulo).font(.headline)
            if conceptos.count > 0 { fila(conceptos[0].nombre, conceptos[0].monto) }
            if conceptos.count > 1 { fila(conceptos[1].nombre, conceptos[1].monto) }
            if conceptos.count > 2 { fila(conceptos[2].nombre, conceptos[2].monto) }
            if conceptos.count > 3 { fila(conceptos[3].nombre, conceptos[3].monto) }
            if conceptos.count > 4 { fila(conceptos[4].nombre, conceptos[4].monto) }
        }.padding().background(.blue.opacity(0.06)).clipShape(.rect(cornerRadius: 12))
    }
    // CONEXIÓN ENTRE PANTALLA Y MODELO:
    // 1. Limpiar el resultado anterior. 2. Convertir y validar las entradas.
    // 3. Pedir el cálculo a Boleta. 4. Guardar el resultado para que SwiftUI lo muestre.
    private func calcular() {
        resultado = nil
        error = ""
        // do/try/catch permite recibir los errores de validación sin cerrar la app.
        do {
            // Entrada.datos convierte los String del formulario en DatosBoleta.
            // Si encuentra algo inválido, lanza un error y pasa al catch.
            let datos = try Entrada.datos(sueldo: sueldo, dias: dias, hijos: hijos, sistema: sistema,
                afp: afp, horas25: horas25, horas35: horas35, adelantos: adelantos)
            // Se crea una calculadora Boleta y se le entregan los datos ya validados.
            // Cambiar resultado hace aparecer la boleta en el bloque if let de arriba.
            resultado = try Boleta().calcular(datos)
            descripcion = "Sueldo S/ \(Dinero.texto(datos.sueldo)) · \(datos.dias) días · Hijos: \(datos.hijos ? "Sí" : "No") · \(datos.sistema.rawValue)\(datos.sistema == .afp ? " / " + datos.afp : "") · HE25: \(datos.horas25) · HE35: \(datos.horas35) · Adelanto S/ \(Dinero.texto(datos.adelantos))"
        // Aquí error es el fallo recibido; self.error es el texto @State que se muestra.
        } catch { self.error = error.localizedDescription }
    }
}
