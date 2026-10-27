// swift-tools-version: 5.9
import PackageDescription
// Este paquete compila el modelo sin SwiftUI para poder probarlo en Windows.
// Para ejecutar la pantalla iOS se abre BoletaPago.xcodeproj en un Mac con Xcode.
let package = Package(
    name: "BoletaPago",
    products: [.library(name: "BoletaCore", targets: ["BoletaCore"])],
    targets: [
        // Reutilizamos el mismo archivo de cálculo que emplea la aplicación.
        .target(name: "BoletaCore", path: "App/Model"),
        // Ejecutable de pruebas: swift run VerificarBoleta.
        .executableTarget(name: "VerificarBoleta", dependencies: ["BoletaCore"], path: "Tests/Verifier")
    ]
)
