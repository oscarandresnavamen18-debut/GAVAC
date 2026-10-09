import '../entities/vacunacion.dart';

abstract class SanidadRepository {
  Future<void> registrarVacunacion(Vacunacion vacunacion);
}
