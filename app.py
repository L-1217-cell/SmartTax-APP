import streamlit as st
import pandas as pd

# 1. 页面全局设置（必须放在第一句）
st.set_page_config(page_title="智慧财税管理智能体", layout="wide")

# 2. 侧边栏：企业画像（对应作业：构建企业画像）
with st.sidebar:
    st.header("🏢 企业基础信息")
    company_name = st.text_input("企业名称", "星辰科技有限公司")
    industry = st.selectbox("所属行业", ["信息技术", "批发零售", "制造业", "其他"])
    scale = st.radio("企业规模", ["小型微利", "一般企业"], horizontal=True)
    st.divider()
    st.info("💡 填写左侧信息后，系统将自动匹配政策并辅助计税。")

# 3. 主页面标题
st.title("📊 智慧财税管理智能体")
st.caption(f"当前登录企业：{company_name} | 行业：{industry} | 规模：{scale}")

# 4. 使用 Tabs 划分四大核心功能模块
tab1, tab2, tab3, tab4 = st.tabs(["📝 自动计税", "📄 申报表生成", "🎯 政策匹配", "⚠️ 风险分析"])

with tab1:
    st.subheader("自动计税引擎")
    
    # 使用两列布局：左边输入，右边输出
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**请输入本期财务数据：**")
        sales = st.number_input("本期销售额（元）", value=1000000.0, step=10000.0)
        purchase = st.number_input("本期进项税额（元）", value=50000.0, step=1000.0)
        
        # 根据规模不同，税率可能不同
        tax_rate = 0.13 
        st.write(f"当前适用增值税率：{tax_rate*100}%")

    with col2:
        st.write("**计税结果：**")
        # 基础规则计算
        output_tax = sales * tax_rate
        payable_tax = output_tax - purchase
        
        if payable_tax < 0:
            payable_tax = 0 
            
        st.metric(label="本期销项税额", value=f"¥ {output_tax:,.2f}")
        st.metric(label="本期应纳增值税", value=f"¥ {payable_tax:,.2f}", delta="需缴纳税款" if payable_tax > 0 else "无需缴税")


    # ---------- 下面是新增的企业所得税计算模块 ----------
    st.divider() # 画一条分割线，把增值税和企业所得税隔开
    
    st.subheader("企业所得税计算")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**请输入本期利润数据：**")
        # 输入利润总额
        profit = st.number_input("本期利润总额（元）", value=500000.0, step=10000.0)
        
        # --- 核心规则引擎：根据左侧侧边栏选择自动匹配税率 ---
        if scale == "小型微利":
            if profit <= 3000000:
                cit_rate = 0.05  # 小微企业实际税负 5%
                policy_note = "（适用小型微利企业优惠：实际税负 5%）"
            else:
                cit_rate = 0.25  # 超过300万，不再享受小微优惠
                policy_note = "（利润超过300万，适用法定税率 25%）"
        elif industry == "信息技术":
            cit_rate = 0.15      # 高新技术企业 15%
            policy_note = "（适用高新技术企业优惠：税率 15%）"
        else:
            cit_rate = 0.25      # 一般企业
            policy_note = "（适用法定税率 25%）"
            
        st.write(f"当前适用税率：**{cit_rate*100}%** {policy_note}")
        
    with col4:
        st.write("**计税结果：**")
        # 计算企业所得税
        cit_tax = profit * cit_rate
        
        # 利润为负不需要交税
        if cit_tax < 0:
            cit_tax = 0
            
        st.metric(label="本期应纳企业所得税", value=f"¥ {cit_tax:,.2f}")
        
        if profit < 0:
            st.info("💡 本期为亏损，无需缴纳企业所得税。")
# ================= 模块二：申报表生成 =================
with tab2:
    st.subheader("申报表预览与导出")
    st.write("根据计算结果自动生成规范申报表：")
    
    # 伪造一个 DataFrame 用作展示（对应作业：输出全套申报表）
    data = {
        "项目": ["销售额", "销项税额", "进项税额", "应纳税额"],
        "金额（元）": [sales, sales*0.13, purchase, max(0, sales*0.13 - purchase)]
    }
    df = pd.DataFrame(data)
    
    # 展示表格
    st.dataframe(df, use_container_width=True)
    
    # 下载按钮（对应作业：支持下载归档）
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ 下载增值税申报表 (CSV)",
        data=csv,
        file_name=f"{company_name}_增值税申报表.csv",
        mime="text/csv",
    )


# ================= 模块三：政策匹配 =================
with tab3:
    st.subheader("税收优惠政策智能推送")
    
    # 简单的 if-else 规则引擎（对应作业：自动识别企业可享受的税费优惠）
    st.write(f"基于您的企业特征（{industry} | {scale}），系统为您匹配到以下政策：")
    
    if scale == "小型微利":
        st.success("✅ 政策一：小型微利企业所得税优惠 —— 实际税负率仅为 5%！")
        st.info("提示：请留存备查企业年度资产负债表、利润表。")
    else:
        st.warning("⏸️ 暂无适用的所得税减免政策，请按 25% 法定税率申报。")
        
    if industry == "信息技术":
        st.success("✅ 政策二：高新技术企业研发费用加计扣除 —— 可按照实际发生额的 100% 在税前加计扣除。")
    

# ================= 模块四：风险分析 =================
with tab4:
    st.subheader("涉税风险预警与分析")
    
    # 简单的规则校验（对应作业：涉税风险分析/智能分类与勾稽校验）
    st.write("正在扫描当前账目数据...")
    
    if purchase > sales * 0.5:
        st.error("🚨 风险警告：本期进项税额占比过高，可能存在进销项不匹配风险，请核实采购发票真实性！")
    else:
        st.success("✅ 风险扫描完成：当前进销项比例正常，未发现明显异常指标。")
        
    st.caption("注：后续可在此模块接入机器学习模型（如随机森林），实现更精准的风险预测。")