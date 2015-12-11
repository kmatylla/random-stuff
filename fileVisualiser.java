import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Iterator;
import java.util.NavigableSet;
import java.util.TreeMap;
import javax.imageio.ImageIO;



public class fileVisualiser {

	File file;
	FileInputStream bytes;
	long size;
	
	static int fixByte(byte b){
		if (b<0) return 256+b;
		return b;
	}
	
	
	public fileVisualiser(String filename)
	{
		file=new File(filename);
		size=file.length();

		try {
			bytes=new FileInputStream(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		 
	}
	
	void reset()
	{
		try {
			bytes.close();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		try {
			bytes=new FileInputStream(file);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void finalize()
	{
		if (bytes!=null){
			try {
				bytes.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public void visValue(int width){
		if (width==0) width=(int) Math.sqrt(size/3);
		int height=(int)size/(3*width)+1;
		BufferedImage img=new BufferedImage(width,height,BufferedImage.TYPE_INT_RGB);
		byte[] rgb = new byte[3];
		 int x=0;
		 int y=0;
	     try {
			while (bytes.read(rgb) == 3) {
				//System.out.println(b);
				img.setRGB(x, y, 65536*fixByte(rgb[0])+255*fixByte(rgb[1])+fixByte(rgb[2]));
				x++;
				if (x==width)
				{
					x=0;
					y++;
				}
			 }
		} catch (IOException e) {
			e.printStackTrace();
		}
	     finally
	     {
	    	 reset();
	     }
	    String path;
		try {
			path = file.getCanonicalPath()+".v.png";
			ImageIO.write(img, "png", new File(path));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	

	public void visXY(){
		BufferedImage imgx=new BufferedImage(256,256,BufferedImage.TYPE_INT_RGB);
	     try {
	    	int x=0;
	    	int y=bytes.read();
			while ((x=bytes.read()) != -1) {
				int col=imgx.getRGB(x, y);
				if (col<0) col+=16777216;
				if (col==0) imgx.setRGB(x, y, 4210752); // gray
				else imgx.setRGB(x, y, col+65536); //+red
				y=x;
			 }
		} catch (IOException e) {
			e.printStackTrace();
		}
	     finally
	     {
	    	 reset();
	     }
	     String path;
			try {
				path = file.getCanonicalPath()+".xy.png";
				ImageIO.write(imgx, "png", new File(path));
			} catch (IOException e) {
				e.printStackTrace();
			}
	}
	
	public void visCompression(int width, boolean withCodes){
		if (width==0) width=(int) Math.sqrt(size);
		int height=(int)size/(width)+1;
		BufferedImage coded=new BufferedImage(width,height,BufferedImage.TYPE_INT_RGB); //IDK... some varied colors i guess?
		BufferedImage entropy=new BufferedImage(width,height,BufferedImage.TYPE_INT_RGB); //red = compressed is bigger; blue = smaller; log (infty -> 255; 1->0;
		try {
			boolean end=false;
			TreeMap <String, int[]> codes = new TreeMap<String, int[]>(); // string -> {code, count, code length}
			byte[] b=new byte[1];
			int counter;
			int position=0;
			for(counter=0 ; counter<256 ; counter++){ //bytes has codes = their value
				String s=""+(char)counter;
				//System.out.println(s);
				codes.put(s, new int[]{counter,0,0});
			}
			int c;
			while (bytes.read(b) == 1) // LZW-ish
			{
				c=fixByte(b[0]);
				StringBuilder match= new StringBuilder("");
				int found[];
				while ((found = codes.get(match.toString()+(char)c)) != null && !end){
					match.append((char)c);
					if (bytes.read(b)!=1) end=true;
					else c=fixByte(b[0]);
				} //b = first non matching; match = match
				if (found == null) found = codes.get(match.toString());
				found[1]++; //? test!
				for (int i=0;i<=match.length();i++)
				{
					int x=position%width;
					int y=position/width;
					coded.setRGB(x, y, found[0]);
					position++;
				}
				if(!end)
				{
					match.append((char)c);
					codes.put(match.toString(), new int[]{counter,0,match.length()});
					counter++;
				}
			}
				//Huffman-ish
			TreeMap<Integer,Integer> codeColors = new TreeMap<Integer,Integer>(); //code -> rgb
			NavigableSet<String> keys = codes.navigableKeySet();
			String k;
			double l2=Math.log(2);
			double logCodes=Math.log(counter-256);
			for (Iterator<String> i = keys.iterator();i.hasNext();){
				k=i.next();
				int[] a=codes.get(k);
				if (a[1]!=0){ //some codes may not occur
					double d=(logCodes-Math.log(a[1]*a[2]))/l2;
					if (d<8){
						d=d/8-1;
					}
					else{
						d=1-8/d;
					} //d (0,1)
					int color=65280; //green
					if (d<0) { // low entropy = blue
						//color += 256*(int)(d*256.0); // substr 0-256 fron green
						//color -= (int)(d*256.0); //add to blue
						color += 255*(int)(d*256.0);
					}
					else{ //high = red
						//color -= 256*(int)(d*256.0);
						//color += 65536*(int)(d*256.0); //add red
						color += 65280*(int)(d*256.0);
					}
					codeColors.put(a[0],color); // counter - #alphabet = # added codes = # codes on output
					}
			}
			//System.out.println(codeColors);
			reset();// make a pic
			int maxPos=position;
			for (position=0; position<maxPos; position++)
			{
				int x=position%width;
				int y=position/width;
				int code=coded.getRGB(x, y);
				if (code<0) code=code+16777216;
				entropy.setRGB(x, y, codeColors.get(code));
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		finally
	     {
	    	 reset();
	     }		
		String path;
		try {
			if (withCodes){
				path = file.getCanonicalPath()+".c.png";
				ImageIO.write(coded, "png", new File(path));
			}
			path = file.getCanonicalPath()+".e.png";
			ImageIO.write(entropy, "png", new File(path));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
	if ((args.length==2) || (args.length==3)){
		int w=0;
		String path=args[1];
		if (args.length==3) {
			w=Integer.parseInt(args[1]);
			path=args[2];
		}
		fileVisualiser fv = new fileVisualiser(path);
		char c=args[0].charAt(0);
		if (c == 'a' ){
			fv.visCompression(w,true);
			System.out.println("1/3 done.");
			fv.visValue(w);
			System.out.println("2/3 done.");
			fv.visXY();
			System.out.println("3/3 done.");
			return;
			}
		if (c == 'e' ){
			fv.visCompression(w,false);
			System.out.println("Done.");
			return;
			}
		if (c == 'v' ){
			fv.visValue(w);
			System.out.println("Done.");
			return;
			}
		if (c == 'x' ){
			fv.visXY();
			System.out.println("Done.");
			return;
			}
		}
		
	System.out.println("Usage: fv mode [width] filename.");
	//System.out.println(""+args.length+" args given");
	System.out.println("Modes: a (all), e (randomness of data), v (bytes as values), x (byte values as position; does not use width)");		
	/*String path="";
	System.out.println("Input filename (or \"q\" to exit).");
	while(path!="q") if(path!="q"){
		path=System.console().readLine();
		fileVisualiser fv = new fileVisualiser(path);
		fv.visCompression(0,true);
		System.out.println("1/3 done.");
		fv.visValue(0);
		System.out.println("2/3 done.");
		fv.visXY();
		System.out.println("3/3 done.");
	}*/
	}

}
