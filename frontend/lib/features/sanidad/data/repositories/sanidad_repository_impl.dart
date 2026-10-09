import '../../domain/entities/vacunacion.dart';
import '../../domain/repositories/sanidad_repository.dart';
import '../models/vacunacion_model.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class SanidadRepositoryImpl implements SanidadRepository {
  final String baseUrl;
  final String token;

  SanidadRepositoryImpl({required this.baseUrl, required this.token});

  @override
  Future<void> registrarVacunacion(Vacunacion vacunacion) async {
    final model = VacunacionModel.fromEntity(vacunacion);
    final response = await http.post(
      Uri.parse("$baseUrl/api/sanidad/"),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
      body: jsonEncode(model.toJson()),
    );

    if (response.statusCode != 201 && response.statusCode != 200) {
      throw Exception("Error al registrar vacunación: ${response.body}");
    }
  }
}
