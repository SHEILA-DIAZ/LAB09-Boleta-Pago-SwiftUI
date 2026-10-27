import SwiftUI

struct ContentView: View {
    @State private var sueldo = "2500"
    @State private var dias = "30"
    @State private var hijos = false
    @State private var sistema = Sistema.onp
    @State private var afp = "Ejemplo"
    @State private var horas25 = "0"
    @State private var horas35 = "0"
    @State private var adelantos = "0"
    @State private var resultado: ResultadoBoleta?
    @State private var error = ""
    @State private var descripcion = ""

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                Text("Boleta de ejemplo").font(.largeTitle).bold()
                Text("Semana 9 · Del sueldo al neto").foregroundStyle(.secondary)
                Text("Perfil de la guía: RMV S/ 1,230. AFP Ejemplo usa tasas de prueba. Sin renta de quinta categoría.")
                    .font(.footnote)
                Text("Datos del mes").font(.title2).bold()
                campo("Sueldo básico (S/)", texto: $sueldo)
                VStack(alignment: .leading) {
                    Text("Días laborados (1–30)")
                    TextField("30", text: $dias).keyboardType(.numberPad).textFieldStyle(.roundedBorder)
                }
                Picker("¿Tiene hijos?", selection: $hijos) {
                    Text("No").tag(false)
                    Text("Sí").tag(true)
                }.pickerStyle(.segmented)
                Text("Sistema de pensiones")
                Picker("Sistema de pensiones", selection: $sistema) {
                    Text("ONP").tag(Sistema.onp)
                    Text("AFP").tag(Sistema.afp)
                }.pickerStyle(.segmented)
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
                Button("Calcular") { calcular() }.buttonStyle(.borderedProminent)
                if !error.isEmpty { Text(error).foregroundStyle(.red).accessibilityLabel("Error: \(error)") }
                if let b = resultado {
                    Text("Resultado del último cálculo").font(.title2).bold()
                    Text(descripcion).font(.footnote)
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

    private func campo(_ titulo: String, texto: Binding<String>) -> some View {
        VStack(alignment: .leading) {
            Text(titulo)
            TextField("0", text: texto).keyboardType(.decimalPad).textFieldStyle(.roundedBorder)
        }
    }
    private func fila(_ nombre: String, _ monto: Decimal) -> some View {
        HStack {
            Text(nombre).frame(maxWidth: .infinity, alignment: .leading)
            Text("S/ \(Dinero.texto(monto))").monospacedDigit()
        }
    }
    // Se escriben las filas explícitamente para respetar los controles vistos en clase.
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
    private func calcular() {
        resultado = nil
        error = ""
        do {
            let datos = try Entrada.datos(sueldo: sueldo, dias: dias, hijos: hijos, sistema: sistema,
                afp: afp, horas25: horas25, horas35: horas35, adelantos: adelantos)
            resultado = try Boleta().calcular(datos)
            descripcion = "Sueldo S/ \(Dinero.texto(datos.sueldo)) · \(datos.dias) días · Hijos: \(datos.hijos ? "Sí" : "No") · \(datos.sistema.rawValue)\(datos.sistema == .afp ? " / " + datos.afp : "") · HE25: \(datos.horas25) · HE35: \(datos.horas35) · Adelanto S/ \(Dinero.texto(datos.adelantos))"
        } catch { self.error = error.localizedDescription }
    }
}
