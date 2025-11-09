import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://127.0.0.1:8000/api";
  String? accessToken;
  String? refreshToken;

  /// ✅ Headers getter (automatically adds token)
  Map<String, String> get headers => {
        'Content-Type': 'application/json',
        if (accessToken != null) 'Authorization': 'Bearer $accessToken',
      };

  /// ✅ Login: gets access + refresh tokens
  Future<bool> login(String username, String password) async {
    final url = Uri.parse("$baseUrl/auth/token/");
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'username': username, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      accessToken = data["access"];
      refreshToken = data["refresh"];
      print("✅ Logged in! Access token: $accessToken");
      return true;
    } else {
      print("❌ Login failed: ${response.body}");
      return false;
    }
  }

  /// ✅ Get available products for consumer
  Future<List<dynamic>> getProducts() async {
    final url = Uri.parse("$baseUrl/products/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load products: ${response.statusCode}");
    }
  }

  /// ✅ Place order
  Future<void> placeOrder(int productId, int quantity) async {
    onPressed: () {
      print("ordering $quantity of ${p["name"]}");
      orderProduct(p["productId"]);
    },

    final url = Uri.parse("$baseUrl/orders/");
    final response = await http.post(
      url,
      headers: headers,
      body: json.encode({
        "product": productId,
        "quantity": quantity,
      }),
    );

    if (response.statusCode != 201 && response.statusCode != 200) {
      throw Exception("Order failed: ${response.body}");
    }
  }

  /// ✅ Get all suppliers
  Future<List<dynamic>> getSuppliers() async {
    final url = Uri.parse("$baseUrl/suppliers/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      print("❌ Failed to load suppliers: ${response.body}");
      throw Exception("Failed to load suppliers");
    }
  }

  /// ✅ Send link request to supplier
  Future<bool> sendLinkRequest(int supplierId) async {
    final url = Uri.parse("$baseUrl/suppliers/links/create/");
    final response = await http.post(
      url,
      headers: headers,
      body: json.encode({'supplier': supplierId}),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      print("✅ Link request sent: ${response.body}");
      return true;
    } else {
      print("❌ Failed to send link request: ${response.body}");
      return false;
    }
  }
}
