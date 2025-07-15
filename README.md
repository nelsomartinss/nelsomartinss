```java
// Seja bem-vindo(a) ao meu GitHub 👋

public class NelsonMartins {

    private String nome = "Nelson Martins";
    private String objetivo = "Conseguir um emprego como desenvolvedor Java Backend";
    private List<String> interesses = Arrays.asList(
        "Java", "Desenvolvimento Back-end", 
    );

    public void sobreMim() {
        System.out.println("💡 Analista e Desenvolvedor de Sistema");
        System.out.println("📌 Programador Back-end Java");
    }

    public void tecnologiasQueEstudo() {
        System.out.println("💻 Java | Spring Boot");
        System.out.println("🛠️ Git | VS Code | IntelliJ IDEA ");
    }

    public static void main(String[] args) {
        NelsonMartins eu = new NelsonMartins();
        eu.sobreMim();
        eu.tecnologiasQueEstudo();
    }
}
