import '../../domain/entities/vacunacion.dart';

class VacunacionModel extends Vacunacion {
  VacunacionModel({
    required super.id,
    required super.animalTag,
    required super.vacunaNombre,
    required super.fechaAplicacion,
    required super.edadAnimalMeses,
  });

  factory VacunacionModel.fromEntity(Vacunacion entity) {
    return VacunacionModel(
      id: entity.id,
      animalTag: entity.animalTag,
      vacunaNombre: entity.vacunaNombre,
      fechaAplicacion: entity.fechaAplicacion,
      edadAnimalMeses: entity.edadAnimalMeses,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "animal_tag": animalTag,
      "vacuna_nombre": vacunaNombre,
      "fecha_aplicacion": fechaAplicacion.toIso8601String(),
      "edad_animal_meses": edadAnimalMeses,
    };
  }
}
