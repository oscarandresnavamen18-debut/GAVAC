import '../entities/vacunacion.dart';
import '../repositories/sanidad_repository.dart';

class RegistrarVacunacionUseCase {
  final SanidadRepository repository;

  RegistrarVacunacionUseCase(this.repository);

  Future<void> call(Vacunacion vacunacion) async {
    // Regla de negocio del dominio: El animal debe tener más de 3 meses
    if (vacunacion.edadAnimalMeses < 3) {
      throw Exception("El animal es demasiado joven para esta vacuna (mínimo 3 meses).");
    }
    await repository.registrarVacunacion(vacunacion);
  }
}
