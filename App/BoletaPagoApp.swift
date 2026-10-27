import SwiftUI

// Este es el punto de entrada de la aplicación: iOS comienza a ejecutarla aquí.
// SwiftUI es la herramienta que usamos para describir lo que aparece en pantalla.
@main
struct BoletaPagoApp: App {
    // WindowGroup crea la ventana de la app y ContentView contiene la pantalla
    // del formulario y la boleta. Los cálculos se encuentran en Model/Boleta.swift.
    var body: some Scene { WindowGroup { ContentView() } }
}
