TITLE high threshold calcium current (L-current)

: 2019: From ModelDB, accession: 3808
: Based on the model by McCormick & Huguenard, J Neurophysiol, 1992
: and errata in https://huguenardlab.stanford.edu/reprints/Errata_thalamic_cell_models.pdf
: Modified cai by Elisabetta Iavarone @ Blue Brain Project
: See PARAMETER section for references 

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX TC_iL
	USEION cal1 READ cal1i,cal1o WRITE ical1
        USEION cal2 READ cal2i,cal2o WRITE ical2
        :USEION cal3 READ cal3i,cal3o WRITE ical3
        :RANGE pcabar1, pcabar2, pcabar3, m_inf, tau_m
        RANGE pcabar1, pcabar2, m_inf, tau_m
        GLOBAL beta



        RANGE output, i_output
}

UNITS {
	(mA)	= (milliamp)
	(mV)	= (millivolt)
	(molar) = (1/liter)
	(mM)	= (millimolar)
        FARADAY = (faraday) (coulomb)
        R       = 8.314 (volt-coul/degC)
}

PARAMETER {
	v			(mV)
	celsius			(degC)
        dt              	(ms)
	cal1i  = 0.5E-4    	(mM) : Value from Amarillo et al., J Neurophysiol, 2014
	cal1o  = 2		(mM)
	cal2i  = 0.5E-4    	(mM) : Value from Amarillo et al., J Neurophysiol, 2014
	cal2o  = 2		(mM)
	:cal3i  = 0.5E-4    	(mM) : Value from Amarillo et al., J Neurophysiol, 2014
	:cal3o  = 2		(mM)
	pcabar1= 1e-4	        (cm/s)
	pcabar2= 1e-4	        (cm/s)
	:pcabar3= 1e-4	        (cm/s)
        beta  = 1
}

STATE {
	m
}

ASSIGNED {
	ical1		(mA/cm2)
	ical2		(mA/cm2)
	:ical3		(mA/cm2)
	i_rec		(mA/cm2)	
	tau_m		(ms)
	m_inf 
	tcorr



        output
        i_output
}

BREAKPOINT { 
	SOLVE states METHOD cnexp


        :output   = (pcabar1+pcabar2+pcabar3)*m*m

        output   = (pcabar1+pcabar2)*m*m

        
	ical1 = pcabar1 * m*m * ghk(v,cal1i,cal1o)
	ical2 = pcabar2 * m*m * ghk(v,cal2i,cal2o)
	:ical3 = pcabar3 * m*m * ghk(v,cal3i,cal3o)
	
        :i_output =ical1+ical2+ical3
        i_output =ical1+ical2
}

DERIVATIVE states {
       rates(v)

       m'= (m_inf-m) / tau_m 
}
  
INITIAL {
	tcorr = 3^((celsius-23.5)/10)
	rates(v)
	m = m_inf



        :output   = (pcabar1+pcabar2+pcabar3)*m*m
        output   = (pcabar1+pcabar2)*m*m
        
	ical1 = pcabar1 * m*m * ghk(v,cal1i,cal1o)
	ical2 = pcabar2 * m*m * ghk(v,cal2i,cal2o)
	:ical3 = pcabar3 * m*m * ghk(v,cal3i,cal3o)
	
        :i_output =ical1+ical2+ical3
        i_output =ical1+ical2
}

UNITSOFF

FUNCTION ghk( v(mV), ci(mM), co(mM))  (millicoul/cm3) {
        LOCAL z, eci, eco
        z = v * (.001) * 2 *FARADAY / (R*(celsius+273.15))
	eco = co*efun(z)
	eci = ci*efun(-z)
	:high cao charge moves inward
	:negative potential charge moves inward
	ghk = (.001)*2*FARADAY*(eci - eco)
}

FUNCTION efun(z) {
	 if (fabs(z) < 1e-4) {
	    efun = 1 - z/2
	 }else{
	    efun = z/(exp(z) - 1)
         }
}

PROCEDURE rates(v(mV)) { LOCAL a,b
	a = 1.6 / (1+ exp(-0.072*(v-5)))
	b = 0.02 * vtrap( -(v-1.31), 5.36)

	tau_m = 1/(a+b) / tcorr
	m_inf = 1/(1+exp((v+10)/-10))
}

FUNCTION vtrap(x,c) { 
	: Traps for 0 in denominator of rate equations
        if (fabs(x/c) < 1e-6) {
          vtrap = c + x/2 }
        else {
          vtrap = x / (1-exp(-x/c)) }
}
UNITSON








