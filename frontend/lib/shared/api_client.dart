import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiClient {
  // En Web usa localhost:8000, en emulador Android usa 10.0.2.2:8000
  static const String baseUrl = "http://localhost:8000";

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('gavac_token');
  }

  static Future<int?> getFincaId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt('gavac_finca_id');
  }

  static Future<Map<String, String>> _headers() async {
    final token = await getToken();
    final fincaId = await getFincaId();
    final headers = <String, String>{
      "Content-Type": "application/json",
    };
    if (token != null) headers["Authorization"] = "Bearer $token";
    if (fincaId != null) headers["X-Finca-ID"] = fincaId.toString();
    return headers;
  }

  static Future<dynamic> get(String endpoint) async {
    final response = await http.get(Uri.parse("$baseUrl$endpoint"), headers: await _headers());
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception("Error GET $endpoint: ${response.body}");
  }

  static Future<dynamic> post(String endpoint, Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse("$baseUrl$endpoint"),
      headers: await _headers(),
      body: jsonEncode(data),
    );
    if (response.statusCode == 200 || response.statusCode == 201) {
      return jsonDecode(response.body);
    }
    throw Exception("Error POST $endpoint: ${response.body}");
  }
}
