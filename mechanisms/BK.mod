NEURON {
	SUFFIX BK
	USEION k READ ek WRITE ik VALENCE 1
	USEION cal2 READ cal2i VALENCE 2
	RANGE gbar, minf, mtau
        RANGE vhalf
        GLOBAL shift
        GLOBAL tau_factor

        RANGE i_output, output
}

UNITS {
	(molar) = (1/liter)
	(mM)	= (millimolar)
	(uM)	= (micromolar)
	(S)  	= (siemens)
	(mA) 	= (milliamp)
	(mV) 	= (millivolt)
}

PARAMETER {
        gbar = 1e-6 (S/cm2)
        shift = 0 (mV)
        tau_factor = 1 (ms)
        q10    = 2.5
        slope = 11.1 (/mV)
        mtau_min = 0.01
        
}

ASSIGNED {
        v       (mV)

        ek (mV)
        ik (mA/cm2)

        i_output
        output


        
		minf
		mtau 	(ms)
		cal2i	(mM)
		celsius	(degC)
		vhalf	(mV)

        q
}

STATE {
        m 
}
 
BREAKPOINT {
        SOLVE states METHOD cnexp
        output    = m*gbar
        i_output  = output*(v-ek)
	ik = i_output
}
 
INITIAL {
		rates(v, cal2i)
		m = minf
                output    = m*gbar
                i_output  = output*(v-ek)
		ik = i_output
                q = q10 ^ ((celsius - 23) / 10)

}

DERIVATIVE states {  
        rates(v, cal2i)
        m' = (minf-m)/mtau
}

FUNCTION sig(x, fmax, xh, f0, k) {
  sig = fmax / ( 1 + exp( (x - xh) / k ) ) + f0
}

FUNCTION alpha(v, k, B) {
  alpha = exp((v - 30) / k) * B
}

FUNCTION beta(v, k, B) {
  if (fabs((v - 30)/k) < 1e-5) {
    beta = 1
  } else {
    beta = -1.0 / ( exp(-(v - 30) / k) - 1) * (v - 30) / k
  }
  beta = beta * B
}


PROCEDURE rates(v(mV), cai (mM)) { LOCAL ca_conc_log, mm, qq, x0, x1, y0, y1, Ba, Bb, a, b, vsh
              vsh = v + shift
                                   
              ca_conc_log = log10(cai) + 3.0            

              Ba = 10 ^ sig(ca_conc_log, 2.53905005,  0.78384945, -1.27772552,  2.04819518)
              Bb = 10 ^ sig(ca_conc_log, 4.07686975,  0.87144064, -3.34336997,  -0.2950530)
              a  = alpha(vsh, -57.82912341, Ba)
              b  = beta(vsh, 26.38506155, Bb)
                                   
              : definition of tau from the literature                              
              mtau = tau_factor / (a + b)

              if(mtau < mtau_min) {
                mtau = mtau_min
              }
                                   
              mtau = mtau / q
                                   

              : Bold line in Figure 2D
              if (ca_conc_log < -0.9) {
                vhalf = 152.0
              } else if (ca_conc_log >= 3.2) {
                vhalf = -47.7
              } else {
                 y0 = 152.0
                 y1 = -47.7
                 x0 = -0.9
                 x1 = 3.2
                 mm = (y1 - y0) / (x1 - x0)
                 qq = - x0 * (y1 - y0) / (x1 - x0) + y0 
                 vhalf = mm * ca_conc_log + qq
              }
              
              minf = 1 / (1 + exp(-(vsh - vhalf)/slope))
}


 
UNITSON 





