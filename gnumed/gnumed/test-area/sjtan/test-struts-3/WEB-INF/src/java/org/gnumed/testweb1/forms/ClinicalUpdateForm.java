/*
 * ClinicalUpdateForm.java
 *
 * Created on July 6, 2004, 12:30 AM
 */

package org.gnumed.testweb1.forms;
import org.apache.struts.action.ActionForm;
import java.util.List;
import java.util.ArrayList;
import org.gnumed.testweb1.data.Vaccination;
import org.apache.commons.logging.LogFactory;
import org.apache.commons.logging.Log;
import org.apache.commons.beanutils.BeanUtils;
import org.gnumed.testweb1.data.DefaultVaccination;
import org.gnumed.testweb1.data.Encounter;

/**
 *
 * @author  sjtan
 */
public class ClinicalUpdateForm extends ActionForm {
    static int updateBatch = 5;
    //List vaccinations = new ArrayList();
    Vaccination[] vaccinations ;
    String test;
    Log log = LogFactory.getLog(this.getClass());
    
    /**
     * Holds value of property encounter.
     */
    private Encounter encounter;
    
    /** Creates a new instance of ClinicalUpdateForm */
    public ClinicalUpdateForm() {
        initVaccinations();
        setEncounter( new Encounter());
    }
    
    private void initVaccinations() {
        vaccinations = new Vaccination[updateBatch];
        for (int i =0; i < updateBatch; ++i) {
            vaccinations[i] = new DefaultVaccination() ;
        }
        log.info("ClinicalForm was initialized");
        
    }
    public Vaccination[] getVaccinations() {
        return (Vaccination[]) vaccinations;
    }
  /*  
    public DefaultVaccination getVaccination(int index) {
        return (DefaultVaccination) vaccinations.get(index);
    }
*/    
    public Vaccination getVaccination(int index) { 
        
        return vaccinations[index];
    }
    
    
    
    
    public void setVaccination( int index, Vaccination v) {
        //Vaccination vo = (Vaccination) vaccinations.get(index);
        try {
            BeanUtils.copyProperties(vaccinations[index], v);
        } catch (Exception e) {
            e.printStackTrace();
           
        }
         log.info("COPIED vaccine="+ vaccinations[index]);
    }
    
    public String getTest() {
        return test;
    }
    public void setTest(String test) {
        this.test=test;
    }
    
    /**
     * Getter for property encounter.
     * @return Value of property encounter.
     */
    public Encounter getEncounter() {
        return this.encounter;
    }
    
    /**
     * Setter for property encounter.
     * @param encounter New value of property encounter.
     */
    public void setEncounter(Encounter encounter) {
        this.encounter = encounter;
    }
    
}
