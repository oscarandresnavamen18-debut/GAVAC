import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/animal.dart';

class ApiService {
  // Cambiar por la IP de tu servidor FastAPI o 10.0.2.2 para emulador Android
  static const String baseUrl = "http://10.0.2.2:8000";

  String? token;
  int? fincaId;

  Map<String, String> get _headers {
    final headers = <String, String>{
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers["Authorization"] = "Bearer $token";
    }
    if (fincaId != null) {
      headers["X-Finca-ID"] = fincaId.toString();
    }
    return headers;
  }

  Future<bool> login(String email, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/api/auth/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"email": email, "password": password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      token = data['access_token'];
      if (data['usuario'] != null && data['usuario']['fincas_autorizadas'] != null) {
        final fincas = data['usuario']['fincas_autorizadas'] as List;
        if (fincas.isNotEmpty) {
          fincaId = fincas[0]['id'];
        }
      }
      return true;
    }
    return false;
  }

  Future<List<Animal>> listarAnimales() async {
    final response = await http.get(
      Uri.parse("$baseUrl/api/ganado/"),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      final List data = jsonDecode(response.body);
      return data.map((json) => Animal.fromJson(json)).toList();
    } else {
      throw Exception("Error al cargar ganado: ${response.body}");
    }
  }
}
