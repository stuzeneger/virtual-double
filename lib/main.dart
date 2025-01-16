import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Digitālais dubultnieks',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  String _response = "Gaidu jautājumu...";
  

  Future<void> _sendMessage(String message) async {
    const String apiUrl = "http://127.0.0.1:8000/"; 
    // const String apiUrl = "https://stuzeneger.pythonanywhere.com/"; 

    

    try {

      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
        body: json.encode({"user_input": message}),
      );


      if (response.statusCode == 200) {
        final data = json.decode(response.body);  
        setState(() {
          // print(response.body);
          _response = data['response'];
        });
      } else {
        setState(() {
          _response = "Kļūda: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        _response = "Notika kļūda: $e";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Eināra Maslinovska digitālais dubultnieks')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  _response,
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
            TextField(
              controller: _controller,
              decoration: InputDecoration(labelText: 'Ievadi savu jautājumu'),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                final message = _controller.text;
                if (message.isNotEmpty) {
                  _sendMessage(message);
                  _controller.clear();
                }
              },
              child: Text('Nosūtīt'),
            ),
          ],
        ),
      ),
    );
  }
}
