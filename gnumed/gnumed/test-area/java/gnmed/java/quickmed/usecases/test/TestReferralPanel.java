/*
 * TestReferralPanel.java
 *
 * Created on 22 August 2003, 22:14
 */

package quickmed.usecases.test;
import org.gnumed.gmIdentity.identity;
import java.text.*;
import java.util.*;
import java.io.*;
import gnmed.test.DomainPrinter;
import javax.print.*;
import javax.print.attribute.*;
import javax.print.attribute.standard.*;
import javax.swing.*;
/**
 *
 * @author  sjtan
 */
public class TestReferralPanel extends javax.swing.JPanel implements ClientProviderRelatable {
    public static final int DEFAULT_PLAINTEXT_LINELEN= 50;
    public static final int DEFAULT_PLAINTEXT_TABSIZE = 8;
    
    
    private ContactsPanel contacts;
    private identity client;
    /** Creates new form TestReferralPanel */
    public TestReferralPanel() {
        initComponents();
        addContactsPanel();
        changeTabNames();
        //        addPrintServiceUI();
        
        setPlainTextLineLength(DEFAULT_PLAINTEXT_LINELEN);
        setPlainTextTabSize(DEFAULT_PLAINTEXT_TABSIZE);
    }
    
    void addContactsPanel() {
        contacts = new ContactsPanel();
        jPanel5.add(contacts);
        validate();
    }
    
    //    void  addPrintServiceUI() {
    //        PrintService service = PrintServiceLookup.lookupDefaultPrintService();
    //        ServiceUIFactory factory = service.getServiceUIFactory();
    //
    //        ServiceUI ui = factory.getUI( factory.MAIN_UIROLE, factory.JCOMPONENT_UI);
    //        jTabbedPane1.addTab(Globals.bundle.getString("print_setup"), ui);
    //    }
    
    void changeTabNames() {
        jTabbedPane1.setTitleAt(0, Globals.bundle.getString("select_contact"));
        jTabbedPane1.setTitleAt(1, Globals.bundle.getString("letter"));
        
    }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    private void initComponents() {//GEN-BEGIN:initComponents
        java.awt.GridBagConstraints gridBagConstraints;

        jPanel1 = new javax.swing.JPanel();
        jLabel1 = new javax.swing.JLabel();
        jTextField1 = new javax.swing.JTextField();
        jButton1 = new javax.swing.JButton();
        jPanel2 = new javax.swing.JPanel();
        generateLetterButton = new javax.swing.JButton();
        jTabbedPane1 = new javax.swing.JTabbedPane();
        jPanel3 = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        jPanel5 = new javax.swing.JPanel();
        jPanel4 = new javax.swing.JPanel();
        jScrollPane2 = new javax.swing.JScrollPane();
        jEditorPane1 = new javax.swing.JEditorPane();
        jPanel6 = new javax.swing.JPanel();
        printButton2 = new javax.swing.JButton();
        saveButton = new javax.swing.JButton();

        setLayout(new java.awt.BorderLayout());

        jPanel1.setLayout(new java.awt.GridBagLayout());

        jLabel1.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("editor_app"));
        jPanel1.add(jLabel1, new java.awt.GridBagConstraints());

        jTextField1.setText("jTextField1");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        jPanel1.add(jTextField1, gridBagConstraints);

        jButton1.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("set_editor"));
        jPanel1.add(jButton1, new java.awt.GridBagConstraints());

        add(jPanel1, java.awt.BorderLayout.NORTH);

        generateLetterButton.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("generate_letter"));
        generateLetterButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                generateLetterButtonActionPerformed(evt);
            }
        });

        jPanel2.add(generateLetterButton);

        add(jPanel2, java.awt.BorderLayout.SOUTH);

        jPanel3.setLayout(new java.awt.BorderLayout());

        jPanel5.setLayout(new javax.swing.BoxLayout(jPanel5, javax.swing.BoxLayout.X_AXIS));

        jScrollPane1.setViewportView(jPanel5);

        jPanel3.add(jScrollPane1, java.awt.BorderLayout.CENTER);

        jTabbedPane1.addTab("tab1", jPanel3);

        jPanel4.setLayout(new java.awt.BorderLayout());

        jScrollPane2.setViewportView(jEditorPane1);

        jPanel4.add(jScrollPane2, java.awt.BorderLayout.CENTER);

        printButton2.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("print"));
        printButton2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                printButton2ActionPerformed(evt);
            }
        });

        jPanel6.add(printButton2);

        saveButton.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("save"));
        jPanel6.add(saveButton);

        jPanel4.add(jPanel6, java.awt.BorderLayout.SOUTH);

        jTabbedPane1.addTab("tab2", jPanel4);

        add(jTabbedPane1, java.awt.BorderLayout.CENTER);

    }//GEN-END:initComponents
    
    private void printButton2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_printButton2ActionPerformed
        // Add your handling code here:
        
        //        PrintService service =  PrintServiceLookup.lookupDefaultPrintService();
        //        PrintRequestAttributeSet aset = new HashPrintRequestHashAttributeSet();
        //         aset.add(MediaSizeName.ISO_A4);
        //        DocPrintJob job = service.createPrintJob();
        //        job.
        
        int x =  ((java.awt.Component)evt.getSource()).getX();
        int y =  ((java.awt.Component)evt.getSource()).getY();
        
        DocFlavor flavor = DocFlavor.INPUT_STREAM.AUTOSENSE;
        
        
        HashPrintRequestAttributeSet attributes = new HashPrintRequestAttributeSet();
        attributes.add( MediaSizeName.ISO_A4);
        attributes.add( MediaSizeName.FOLIO);
        
        
        
        PrintService[] services = PrintServiceLookup.lookupPrintServices(flavor, attributes);
        if (services == null || services.length == 0) {
            services = new PrintService[] { PrintServiceLookup.lookupDefaultPrintService() };
            
        }
        for (int j = 0; j < services.length; ++j) {
            System.out.println("SERVICE = " + services[j].getName() );
            DocFlavor [] supported = services[j].getSupportedDocFlavors();
            for (int i = 0; i < supported.length; ++i) {
                System.out.println("SUPPORTED FLAVORS = " +
                supported[i].hostEncoding + ",  "+
                supported[i].getClass().getName() + " , " +
                supported[i].getRepresentationClassName() );
            }
        }
        
        
        
        PrintService service = ServiceUI.printDialog(null,
        x, y,
        services, null,  flavor,   attributes);
        if (service != null) try {
            DocPrintJob job = service.createPrintJob();
            String filename = "./tmp.txt";
            FileWriter w = new FileWriter(filename);
            PrintWriter pw = new PrintWriter( w);
            pw.println(transformToPlatformNewlines(getLetter()))   ;
            pw.close();
            FileInputStream fis = new FileInputStream( filename);
            //            PipedInputStream is = new PipedInputStream();
            //            BufferedInputStream bis = new BufferedInputStream(is);
            //            PipedOutputStream os = new PipedOutputStream();
            //            final PrintStream ps = new PrintStream(os, true);
            //            is.connect(os);
            //            new Thread( new Runnable() {
            //                public void run() {
            //                    ps.println(getLetter());
            //                    ps.close();
            //                }
            //            } ).start();
            SimpleDoc doc = new SimpleDoc( fis , flavor ,null);
            job.print( doc, attributes);
        } catch (Exception e) {
            e.printStackTrace();
            JOptionPane.showInternalMessageDialog(JOptionPane.getDesktopPaneForComponent(this), Globals.bundle.getString("print_error") +": "+ e.toString() );
        }
        
    }//GEN-LAST:event_printButton2ActionPerformed
    
    private void generateLetterButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_generateLetterButtonActionPerformed
        // Add your handling code here:
        try {
            generateReferralFile();
        } catch (Exception e)  {
            e.printStackTrace();
        }
        
        
    }//GEN-LAST:event_generateLetterButtonActionPerformed
    
    
    public org.gnumed.gmIdentity.identity getClient() {
        return client;
    }
    
    public org.gnumed.gmIdentity.identity getProvider() {
        return contacts.getSelectedProvider();
    }
    
    public void setClient(org.gnumed.gmIdentity.identity client) {
        this.client = client;
    }
    
    public void setProvider(org.gnumed.gmIdentity.identity provider) {
        // ? implement
        
    }
    
    
    final static String referralFormatString = "\n\n{0, date}\n\n\n{1},\n{2},\n{3}, {4}.\n\n{5},\n{6}\n\n{7}\n\n\t\t\t{8}";
    
    public void generateReferralFile()  throws Exception {
        if (getClient().getPersister() instanceof ManagerReference) {
            ManagerReference ref = ( ManagerReference) getClient().getPersister();
            net.sf.hibernate.Session sess = ref.getGISManager().getSession();
            if (!sess.isConnected())
                sess.reconnect();
            
        }
        
        StringBuffer sb = new StringBuffer();
        org.gnumed.gmGIS.address a = getProvider().findIdentityAddressByAddressType(TestGISManager.homeAddress).getAddress();
        String street = new StringBuffer().append(a.getNumber()).append(", ").append(a.getStreet().getName()).toString();
        String urb = a.getStreet().getUrb().getName();
        String state = a.getStreet().getUrb().getState().getName();
        String postcode = a.getStreet().getUrb().getPostcode();
        MessageFormat mf2 = new MessageFormat(Globals.bundle.getString("neutral_greetings_format"));
        
        String greetings = mf2.format(
        new Object[] {        getProvider().findNames(0).getFirstnames() ,getProvider().findNames(0).getLastnames() });
        
        MessageFormat mf3 = new MessageFormat(Globals.bundle.getString("basic_spiel_format"));
        String spiel = mf3.format(
        new Object[] { getClient().findNames(0).getFirstnames(), getClient().findNames(1).getLastnames(), getClient().getDob() } );
        
        
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        PrintStream ps = new PrintStream( bos);
        
        DomainPrinter.getInstance().printIdentity(ps, getClient());
        String summary = bos.toString();
        String salutations = Globals.bundle.getString("salutations");
        
        MessageFormat mf = new MessageFormat(referralFormatString);
        
        String letter = mf.format( new Object[] { new Date(), street, urb, state, postcode, greetings , spiel, summary, salutations }  );
        
        
        
        // create title
        org.gnumed.gmIdentity.Names cn = getClient().findNames(0);
        
        sb.append(cn.getLastnames()).append('_').append(cn.getFirstnames()).append('_');
        sb.append(DateFormat.getDateTimeInstance(DateFormat.SHORT, DateFormat.SHORT).format(new Date()));
        sb.append(".txt");
        for (int i = 0; i < sb.length(); ++i)
            if (Character.isSpaceChar(sb.charAt(i)) )
                sb.setCharAt(i, '_');
        
        setReferralFilename(sb.toString());
        //        File path = new File(".", getReferralFilename());
        //        path.createNewFile();
        //
        //        OutputStream fos =  new BufferedOutputStream(new FileOutputStream(path));
        //        PrintStream ps2 = new PrintStream(fos);
        //         ps2.println(letter);
        //
        //        fos.close();
        setLetter(wordWrap(letter, getPlainTextLineLength(), getPlainTextTabSize()) );
        jEditorPane1.setText(getLetter());
        jTabbedPane1.setSelectedIndex(1);
    }
    
    public String transformToPlatformNewlines(String letter) {
        
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        PrintStream ps = new PrintStream( bos);
        
        // transform /n to platform specific newline
        for (int j = 0;j < letter.length(); ++j) {
            if (letter.charAt(j) == '\n') {
                ps.println();
            }
            ps.print(letter.charAt(j));
        }
        return  bos.toString();
    }
    
    public String wordWrap( String letter , int triggerLineLength, int tabSize) {
        int len = 0;
        StringBuffer buf = new StringBuffer();
        for (int j = 0;j < letter.length(); ++j) {
            if (letter.charAt(j) == '\t')
                len += tabSize;
            else
                if (letter.charAt(j) == '\n')
                    len = 0;
            if (len >= triggerLineLength
            && ( Character.isISOControl(letter.charAt(j)) ||
            Character.isWhitespace(letter.charAt(j) ) )  ) {
                buf.append("\n");
                len = 0;
                continue;
            }
            
            buf.append(letter.charAt(j));
        }
        return buf.toString();
    }
    /** Getter for property referralFilename.
     * @return Value of property referralFilename.
     *
     */
    public String getReferralFilename() {
        return this.referralFilename;
    }
    
    /** Setter for property referralFilename.
     * @param referralFilename New value of property referralFilename.
     *
     */
    public void setReferralFilename(String referralFilename) {
        this.referralFilename = referralFilename;
    }
    
    /** Getter for property letter.
     * @return Value of property letter.
     *
     */
    public String getLetter() {
        return this.letter;
    }
    
    /** Setter for property letter.
     * @param letter New value of property letter.
     *
     */
    public void setLetter(String letter) {
        this.letter = letter;
    }
    
    /** Getter for property plainTextLineLength.
     * @return Value of property plainTextLineLength.
     *
     */
    public int getPlainTextLineLength() {
        return this.plainTextLineLength;
    }
    
    /** Setter for property plainTextLineLength.
     * @param plainTextLineLength New value of property plainTextLineLength.
     *
     */
    public void setPlainTextLineLength(int plainTextLineLength) {
        this.plainTextLineLength = plainTextLineLength;
    }
    
    /** Getter for property plainTextTabSize.
     * @return Value of property plainTextTabSize.
     *
     */
    public int getPlainTextTabSize() {
        return this.plainTextTabSize;
    }
    
    /** Setter for property plainTextTabSize.
     * @param plainTextTabSize New value of property plainTextTabSize.
     *
     */
    public void setPlainTextTabSize(int plainTextTabSize) {
        this.plainTextTabSize = plainTextTabSize;
    }
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton generateLetterButton;
    private javax.swing.JButton jButton1;
    private javax.swing.JEditorPane jEditorPane1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel3;
    private javax.swing.JPanel jPanel4;
    private javax.swing.JPanel jPanel5;
    private javax.swing.JPanel jPanel6;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JTabbedPane jTabbedPane1;
    private javax.swing.JTextField jTextField1;
    private javax.swing.JButton printButton2;
    private javax.swing.JButton saveButton;
    // End of variables declaration//GEN-END:variables
    
    /** Holds value of property referralFilename. */
    private String referralFilename;
    
    /** Holds value of property letter. */
    private String letter;
    
    /** Holds value of property plainTextLineLength. */
    private int plainTextLineLength;
    
    /** Holds value of property plainTextTabSize. */
    private int plainTextTabSize;
    
}
