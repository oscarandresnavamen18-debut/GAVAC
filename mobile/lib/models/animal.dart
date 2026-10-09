class Animal {
  final int id;
  final String tag;
  final String? nombre;
  final String especie;
  final String? raza;
  final String? sexo;
  final double? pesoActual;
  final int? edadMeses;
  final String? lote;
  final String status;

  Animal({
    required this.id,
    required this.tag,
    this.nombre,
    required this.especie,
    this.raza,
    this.sexo,
    this.pesoActual,
    this.edadMeses,
    this.lote,
    required this.status,
  });

  factory Animal.fromJson(Map<String, dynamic> json) {
    return Animal(
      id: json['id'],
      tag: json['tag'],
      nombre: json['nombre'],
      especie: json['especie'] ?? 'Bovino',
      raza: json['raza'],
      sexo: json['sexo'],
      pesoActual: json['peso_actual'] != null ? (json['peso_actual'] as num).toDouble() : null,
      edadMeses: json['edad_meses'],
      lote: json['lote'],
      status: json['status'] ?? 'active',
    );
  }
}
