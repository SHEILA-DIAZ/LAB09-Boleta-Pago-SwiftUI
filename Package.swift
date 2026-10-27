// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "BoletaPago",
    products: [.library(name: "BoletaCore", targets: ["BoletaCore"])],
    targets: [
        .target(name: "BoletaCore", path: "App/Model"),
        .executableTarget(name: "VerificarBoleta", dependencies: ["BoletaCore"], path: "Tests/Verifier")
    ]
)
