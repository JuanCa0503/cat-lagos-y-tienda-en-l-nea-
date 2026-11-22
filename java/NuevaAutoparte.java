import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Locale;

public class NuevaAutoparte {

    // Reemplaza con tus datos de Supabase (Settings > API)
    private static final String SUPABASE_URL = "https://TU_PROYECTO.supabase.co";
    private static final String SUPABASE_API_KEY = "TU_ANON_KEY_DE_SUPABASE";

    private static String escaparJson(String texto) {
        if (texto == null) return "";
        return texto.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    public static boolean insertarAutoparte(
            String codigoSku,
            String nombre,
            String categoria,
            double precio,
            int stock
    ) {
        String endpoint = SUPABASE_URL + "/rest/v1/autopartes";

        String jsonBody = String.format(
                Locale.US,
                "{\"codigo_sku\":\"%s\",\"nombre\":\"%s\",\"categoria\":\"%s\",\"precio\":%.2f,\"stock\":%d}",
                escaparJson(codigoSku),
                escaparJson(nombre),
                escaparJson(categoria),
                precio,
                stock
        );

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(endpoint))
                .header("apikey", SUPABASE_API_KEY)
                .header("Authorization", "Bearer " + SUPABASE_API_KEY)
                .header("Content-Type", "application/json")
                .header("Prefer", "return=representation")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() >= 200 && response.statusCode() < 300) {
                System.out.println("Autoparte guardada correctamente.");
                System.out.println("Respuesta de Supabase: " + response.body());
                return true;
            } else {
                System.err.println("Error al insertar autoparte. Código HTTP: " + response.statusCode());
                System.err.println("Detalle: " + response.body());
                return false;
            }
        } catch (Exception e) {
            System.err.println("Excepción al conectar con Supabase: " + e.getMessage());
            return false;
        }
    }

    public static void main(String[] args) {
        insertarAutoparte(
                "FIL-ACE-011",
                "Filtro de Aceite Original",
                "Filtros",
                290.00,
                18
        );
    }
}
