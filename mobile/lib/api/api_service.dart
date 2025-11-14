import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = "http://localhost:8000/api";

  String? accessToken;
  String? refreshToken;
  int? loggedInUserId;
  int? salesmanId;

  Map<String, String> get headers => {
        'Content-Type': 'application/json',
        if (accessToken != null) 'Authorization': 'Bearer $accessToken',
      };

  // ---------------- LOGIN ----------------
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
      loggedInUserId = data["user_id"];

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("accessToken", accessToken!);
      await prefs.setString("refreshToken", refreshToken!);
      await prefs.setInt("loggedInUserId", loggedInUserId!);

      print("✅ Logged in! Access token: $accessToken");
      return true;
    } else {
      print("❌ Login failed: ${response.body}");
      return false;
    }
  }

  // ---------------- TOKEN LOAD ----------------
  Future<void> loadTokens() async {
    final prefs = await SharedPreferences.getInstance();
    accessToken = prefs.getString("accessToken");
    refreshToken = prefs.getString("refreshToken");
    loggedInUserId = prefs.getInt("loggedInUserId");

    print("🔄 Loaded saved tokens: $accessToken");
  }

  // ---------------- LOGOUT ----------------
  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove("accessToken");
    await prefs.remove("refreshToken");
    await prefs.remove("loggedInUserId");

    accessToken = null;
    refreshToken = null;
    loggedInUserId = null;

    print("🔒 Logged out");
  }

  // ---------------- PRODUCTS ----------------
  Future<List<dynamic>> getProducts() async {
    final url = Uri.parse("$baseUrl/products/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load products: ${response.statusCode}");
    }
  }

  Future<void> placeOrder(int productId, int quantity) async {
    final url = Uri.parse("$baseUrl/orders/");
    final response = await http.post(
      url,
      headers: headers,
      body: json.encode({
        "product": productId,
        "quantity": quantity,
      }),
    );

    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception("Order failed: ${response.body}");
    }
  }

  // ---------------- SUPPLIERS ----------------
  Future<List<dynamic>> getSuppliers() async {
    final url = Uri.parse("$baseUrl/suppliers/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load suppliers");
    }
  }

  Future<List<dynamic>> getMySuppliers() async {
    final url = Uri.parse("$baseUrl/users/my-suppliers/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load linked suppliers");
    }
  }

  Future<bool> sendLinkRequest(int supplierId) async {
    final url = Uri.parse("$baseUrl/suppliers/links/create/");
    final response = await http.post(
      url,
      headers: headers,
      body: json.encode({'supplier': supplierId}),
    );

    return response.statusCode == 200 || response.statusCode == 201;
  }

  // ---------------- SALESMAN ----------------
  Future<void> fetchSalesman() async {
    final url = Uri.parse("$baseUrl/users/my-salesman/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      salesmanId = data["salesman_id"];
      print("📌 Salesman ID loaded: $salesmanId");
    }
  }

  Future<int?> fetchSalesmanForSupplier(int supplierId) async {
    final url = Uri.parse("$baseUrl/users/salesman/$supplierId/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data["salesman_id"];
    } else {
      return null;
    }
  }

  // ---------------- CHAT ----------------
  Future<List<dynamic>> getChatHistory(int otherUserId) async {
    final url = Uri.parse("$baseUrl/chat/history/$otherUserId/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load chat history");
    }
  }

  Future<void> sendMessage(int receiverId, String content) async {
    final url = Uri.parse("$baseUrl/chat/send/");
    final response = await http.post(
      url,
      headers: headers,
      body: json.encode({
        "receiver": receiverId,
        "content": content,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception("Failed to send message");
    }
  }

  // ---------------- LOAD PRODUCTS ----------------
  Future<List<dynamic>> getProductsBySupplier(int supplierId) async {
    final url = Uri.parse("$baseUrl/products/by-supplier/$supplierId/");
    final response = await http.get(url, headers: headers);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load products from supplier");
    }
  }
}


